FROM ruby:3.3.12-bookworm

RUN apt-get update \
    && apt-get install -y --no-install-recommends nodejs npm python3 python3-venv \
    && rm -rf /var/lib/apt/lists/*

ENV GEM_HOME=/usr/gem
ENV VIRTUAL_ENV=/opt/venv
ENV PATH="/opt/venv/bin:/usr/gem/bin:$PATH"

RUN gem install bundler -v 2.6.3 \
    && bundle config --global frozen 1 \
    && python3 -m venv "$VIRTUAL_ENV"

WORKDIR /srv/portal

COPY Gemfile Gemfile.lock package.json package-lock.json requirements.txt ./
RUN bundle install \
    && pip install --no-cache-dir -r requirements.txt

COPY . .
RUN npm run build

RUN git config --global --add safe.directory /srv/portal

CMD ["bundle", "exec", "jekyll", "serve", "--host", "0.0.0.0"]
