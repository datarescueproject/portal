import pandas as pd
import re
import os


def slugify(string):
    string = clean_text(string)
    # Remove special characters
    string = re.sub(r'[^\w\s-]', '', string)
    # Replace spaces with hyphens
    string = re.sub(r'\s+', '-', string)
    # Convert to lowercase
    string = string.lower()
    return string


def clean_text(string):
    # Remove URL prefixes like http:// or https://
    # string = re.sub(r'http[s]?://', '', string)
    # Remove escape strings like \n
    string = string.replace('\n', '').replace('\r', '').replace('\t', '')
    # Remove multiple spaces
    string = re.sub(r'\s+', ' ', string)
    # Remove leading spl. characters
    string = re.sub(r'^[^a-zA-Z0-9]+', '', string)
    string = re.sub(r'^-', '', string)
    # Remove leading and trailing ':'
    string = string.rstrip(':')
    string = re.sub(r'(?<!http)(?<!https):', '', string)

    return string


def remove_files_os(dir_path):
    for filename in os.listdir(dir_path):
        file_path = os.path.join(dir_path, filename)
        if os.path.isfile(file_path):
            os.remove(file_path)


def get_metadata_availability(dataset_id, data_backups):
    """
    This function checks the metadata availability for dataset_id 432 in the backups dataframe.
    It returns "Yes" if metadata is available, "Under Review" if it needs review, and "No" otherwise.
    """
    md_avl = data_backups[data_backups.dataset_id == dataset_id].metadata_available.values
    if "yes" in md_avl:
        return "Yes", data_backups[data_backups.dataset_id == dataset_id].metadata_url.values[0]
    elif "needs review" in md_avl:
        return "Under Review", ""
    else:
        return "No", ""


def get_dataset_category(row, organizations):
    # Check if dataset has category override
    categories = eval(row['categories'])
    if categories:
        cats = [a['value'] for a in categories]
    # Check if we don't have organization info
    elif row['organization'] == 'Unknown':
        cats = ['Uncategorized']
    else:
        # Get categories from organization
        cats_from_org = organizations[organizations['Organizations'] == row['organization']]['Categories'].values
        cats = []
        [cats.extend(v.split(';')) for v in cats_from_org]      
        cats = list(set(cats))
        if cats == ['']:
            cats = ['Uncategorized']
        else:
            cats = [cat for cat in cats if cat != '']

    return cats


def create_category_md(row):
    cat_path = "./_dataset_categories"
    cat_filename = slugify(row['Name'])
    # Creating the category markdown file
    cat_md = "---\n"
    cat_md += f"name: {row['Name']} \n" 
    cat_md += f"logo: /img/categories_updated/{cat_filename}.svg \n" 
    cat_md += f"featured: {row['Active']} \n" 
    cat_md += "---\n"

    # Writing the catanization markdown file
    with open(f'{cat_path}/{cat_filename}.md', 'w') as output:
        output.write(cat_md)


def create_dataset_md(row, backups, organizations):
    if row['organization'] == '':
        row['organization'] = 'Unknown'
    # Defining the schema, filename and path
    schema = 'data_rescue_project'
    dataset_filename = slugify(row['dataset'])
    dataset_path = "./_datasets"

    org_path = "./_organizations"

    # Get backups for each dataset
    data_backups = backups[backups.dataset == row['dataset']]
    metadata_available, metadata_url = get_metadata_availability(row['dataset_id'], data_backups)
    # Creating the dataset markdown file
    # Dataset-level information
    dataset_md = "---\n"
    dataset_md += f"schema: {schema} \n"
    dataset_md += f"title: {clean_text(row['dataset'])}\n"
    dataset_md += f"organization: {clean_text(row['organization'])}\n"
    dataset_md += f"agency: {clean_text(row['agency'])}\n"
    dataset_md += f"websites: {clean_text(row['websites'])}\n"
    dataset_md += f"data_source: {clean_text(row['url'])}\n"
    dataset_md += f"description: {clean_text(row['notes'])}\n"
    dataset_md += f"last_modified: {row['last_modified']}\n"
    # Check if any backups have metadata available and populate
    dataset_md += f"metadata_available: {metadata_available}\n"
    dataset_md += f"metadata_url: {clean_text(metadata_url)}\n"
    dataset_md += "category:\n"
    cats = get_dataset_category(row, organizations)

    for cat in cats:
        dataset_md += f"  - {cat} \n"

    dataset_md += "resources:\n"
    # Resource-level information
    for index, backup_row in data_backups.iterrows():
        dataset_md += f"  - id: {index}\n"
        dataset_md += f"    url: {clean_text(backup_row['download_location'])}\n"
        dataset_md += f"    format: {clean_text(backup_row['file_type'])}\n"
        dataset_md += f"    status: {clean_text(backup_row['status'])}\n"
        dataset_md += f"    size: {backup_row['size']}\n"
        dataset_md += f"    download_date: {backup_row['download_date']}\n"
        dataset_md += f"    maintainer: {clean_text(backup_row['maintainer'])}\n"
        dataset_md += f"    notes: {clean_text(backup_row['notes'])}\n"
    dataset_md += "---\n"

    # Writing the dataset markdown file
    with open(f'{dataset_path}/{dataset_filename}.md', 'w') as output:
        output.write(dataset_md)

    # Creating the organization markdown file
    org_filename = slugify(row['organization'])
    org_md = "---\n"
    org_md += f"title: {clean_text(row['organization'])} \n" 
    org_md += "description: \n" 
    org_md += "---\n"

    # Writing the organization markdown file
    with open(f'{org_path}/{org_filename}.md', 'w') as output:
        output.write(org_md)

    agency_path = "./_agencies"
    agency_filename = slugify(row['agency'])

    # Creating the agency markdown file
    agency_md = "---\n"
    agency_md += f"title: {clean_text(row['agency'])} \n"
    agency_md += "description: \n"
    agency_md += "---\n"

    # Writing the agency markdown file
    with open(f'{agency_path}/{agency_filename}.md', 'w') as output:
        output.write(agency_md)


def create_agency_md(row):
    """
    This function creates a markdown file for each agency.
    """


def create_markdowns():
    """
    This function creates markdown files for each dataset and organization.
    """
    backups = pd.read_csv("https://raw.githubusercontent.com/datarescueproject/portal/refs/heads/main/baserow_exports/datarescue_backups.csv")
    datasets = pd.read_csv("https://raw.githubusercontent.com/datarescueproject/portal/refs/heads/main/baserow_exports/datarescue_datasets.csv")
    organizations = pd.read_csv("https://raw.githubusercontent.com/datarescueproject/portal/refs/heads/main/baserow_exports/datarescue_organizations.csv")
    # agencies = pd.read_csv("https://raw.githubusercontent.com/datarescueproject/portal/refs/heads/main/baserow_exports/datarescue_agencies.csv")
    categories = pd.read_csv("https://raw.githubusercontent.com/datarescueproject/portal/refs/heads/main/baserow_exports/datarescue_categories.csv")
    categories['Active'] = categories['Active'].astype(str).str.lower()

    backups.columns = backups.columns.str.lower()
    backups = backups.fillna('')
    backups.head()

    datasets.columns = datasets.columns.str.lower()
    datasets = datasets.fillna('')
    datasets.head()

    organizations = organizations.fillna('')
    # Remove files in _datasets and _organizations
    remove_files_os('./_datasets')
    remove_files_os('./_organizations')
    remove_files_os('./_dataset_categories')
    remove_files_os('./agencies')

    categories.apply(create_category_md, axis=1)
    datasets.apply(create_dataset_md, axis=1, args=(backups, organizations))
