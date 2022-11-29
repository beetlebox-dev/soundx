from flask import Flask, render_template, request, url_for, redirect
from ferry import render_home_template, render_results_template
from admin import admin_alert_thread


# Copyright 2021 Johnathan Pennington | All rights reserved.


app = Flask(__name__)


@app.errorhandler(404)
def page_not_found(e):

    skip_endpoints = ('ferry_query',)
    ignore_paths_starting_with = [  # Doesn't send an admin alert if request.path starts with any of these.
        '20', 'admin', 'blog', 'cms', 'feed', 'media', 'misc', 'news', 'robots', 'site', 'sito',
        'shop', 'test', 'web', 'wordpress', 'Wordpress', 'wp', 'Wp', 'xmlrpc.php',
    ]
    site_root = url_for('ferry', _external=True).split('//', 1)[-1][:-1]
    # Siteroot includes domain, but removes http:// or https:// if present, and removes the final forward slash.
    a_text = site_root
    rel_path = '/'

    request_of_concern = True
    for path_to_ignore in ignore_paths_starting_with:
        if request.path.startswith(f'/{path_to_ignore}'):
            request_of_concern = False
            break

    if request_of_concern:

        for rule in app.url_map.iter_rules():
            if "GET" in rule.methods and rule.endpoint not in skip_endpoints and len(rule.arguments) == 0:
                # Static folder has rule.arguments, so is skipped and rerouted to root.
                if request.path.startswith(rule.rule):  # Rule.rule is relative path.
                    rel_path = url_for(rule.endpoint)
                    if rel_path == '/':
                        continue  # Otherwise, displays final slash after site root <a> text.
                    a_text = f'{site_root}<wbr>{rel_path}'
                    break

        message_body = f'Page not found: \n{request.url}\n' \
                       f'Rendered page_not_found.html and suggested: \n{site_root}{rel_path}'
        admin_alert_thread('Web App - 404', message_body)

    return render_template('page_not_found.html', relpath=rel_path, a_text=a_text), 404


@app.route('/favicon.ico')
def favicon():
    return redirect(url_for('static', filename='favicon.ico'))


# FERRY ROUTES:

@app.route('/')
def ferry():
    return render_home_template()


@app.route('/query')
def ferry_query():
    if 'origin' in request.args:
        origin = request.args['origin']
    else:
        origin = ''
    if 'destination' in request.args:
        destination = request.args['destination']
    else:
        destination = ''
    return render_results_template(origin, destination)


if __name__ == '__main__':
    app.run()
