#!/usr/bin/env python
# encoding: utf-8
#
# This file is part of ckanext-query-dois
# Created by the Natural History Museum in London, UK

import copy
import itertools
import json
import operator
from collections import OrderedDict
from functools import partial
from urllib.parse import urlencode

from ckan import model
from ckan.plugins import toolkit

from ..lib.stats import DOWNLOAD_ACTION, SAVE_ACTION
from ..lib.utils import get_resource_and_package
from ..model import QueryDOI, QueryDOIStat

column_param_mapping = (
    ('doi', QueryDOIStat.doi),
    ('identifier', QueryDOIStat.identifier),
    ('domain', QueryDOIStat.domain),
    ('action', QueryDOIStat.action),
)


def get_query_doi(doi):
    """
    Retrieves a QueryDOI object from the database for the given DOI, if there is one,
    otherwise returns None.

    :param doi: the doi (full doi, prefix/suffix)
    :returns: A QueryDOI object or None
    """
    return model.Session.query(QueryDOI).filter(QueryDOI.doi == doi).first()


def get_authors(packages):
    """
    Retrieves all the authors from the given packages, de-duplicates them (if necessary)
    and then returns them as a list.

    Note that this function takes a list of packages as it is multi-package and
    therefore multi-resource ready.

    :param packages: the packages
    :returns: a list of author(s)
    """
    # use an ordered dict in the absence of a sorted set
    authors = OrderedDict()
    for package in packages:
        author = package['author']
        # some author values will contain many authors with a separator, perhaps , or ;
        for separator in (';', ','):
            if separator in author:
                authors.update({a: True for a in author.split(separator)})
                break
        else:
            # if the author value didn't contain a separator then we can just use the value as is
            authors[author] = True

    return list(authors.keys())


def encode_params(params, version=None, extras=None, for_api=False):
    """
    Encodes the parameters for a query in the CKAK resource view format and returns as a
    query string.

    :param params: a dict of parameters, such as a DatastoreQuery's query dict
    :param version: the version to add into the query string (default: None)
    :param extras: an optional dict of extra parameters to add as well as the ones found
        in the params dict (default: None)
    :param for_api: whether the query string is for a CKAN resource view or an API get
        as it changes the format (default: False)
    :returns: a query string of the query parameters (no ? at the start but will include
        & if needed)
    """
    query_string = {}
    extras = [] if extras is None else extras.items()
    # build the query string from the dicts we have first
    for param, value in itertools.chain(params.items(), extras):
        # make sure to ignore all version data in the dicts
        if param == 'version':
            continue
        if param == 'filters':
            value = copy.deepcopy(value)
            if version is None:
                value.pop('__version__', None)
        query_string[param] = value

    # now add the version in if needed
    if version is not None:
        query_string.setdefault('filters', {})['__version__'] = version

    # finally format any nested dicts correctly (this is for the filters field basically)
    for param, value in query_string.items():
        if isinstance(value, dict):
            if for_api:
                # the API takes the data in JSON format so we just need to serialise it
                value = json.dumps(value)
            else:
                # if the data is going in a query string for a resource view it needs to be
                # encoded in a special way
                parts = []
                for sub_key, sub_value in value.items():
                    if not isinstance(sub_value, list):
                        sub_value = [sub_value]
                    parts.extend('{}:{}'.format(sub_key, v) for v in sub_value)
                value = '|'.join(parts)
            query_string[param] = value

    return urlencode(query_string)


def generate_rerun_urls(resource, package, query, rounded_version):
    """
    Generate a dict containing all the "rerun" URLs needed to allow the user to revisit the data
    either through the website or through the API. The dict returned will look like following:

        {
            "page": {
                "original": ...
                "current": ...
            },
            "api": {
                "original": ...
                "current": ...
            }
        }

    :param resource: the resource dict
    :param package: the package dict
    :param query: the query dict
    :param rounded_version: the version rounded down to the nearest available on the resource
    :returns: a dict of urls
    """
    page_url = toolkit.url_for(
        'resource.read', id=package['name'], resource_id=resource['id']
    )
    api_url = '/api/action/datastore_search'
    api_extras = {'resource_id': resource['id']}
    return {
        'page': {
            'original': page_url + '?' + encode_params(query, version=rounded_version),
            'current': page_url + '?' + encode_params(query),
        },
        'api': {
            'original': api_url
            + '?'
            + encode_params(
                query, version=rounded_version, extras=api_extras, for_api=True
            ),
            'current': api_url
            + '?'
            + encode_params(query, extras=api_extras, for_api=True),
        },
    }


def get_stats(query_doi):
    """
    Retrieve some simple stats about the query DOI - this includes the total downloads and the
    last download timestamp. Note that we are specifically looking for downloads here, no other
    actions are considered.

    :param query_doi: the QueryDOI object
    :returns: a 3-tuple containing the total downloads, total saves and the last download timestamp
    """
    # count how many download stats we have on this doi
    download_total = (
        model.Session.query(QueryDOIStat)
        .filter(QueryDOIStat.doi == query_doi.doi)
        .filter(QueryDOIStat.action == DOWNLOAD_ACTION)
        .count()
    )
    # count how many save stats we have on this doi
    save_total = (
        model.Session.query(QueryDOIStat)
        .filter(QueryDOIStat.doi == query_doi.doi)
        .filter(QueryDOIStat.action == SAVE_ACTION)
        .count()
    )
    # find the last stats object we have for this doi
    last = (
        model.Session.query(QueryDOIStat)
        .filter(QueryDOIStat.doi == query_doi.doi)
        .filter(QueryDOIStat.action == DOWNLOAD_ACTION)
        .order_by(QueryDOIStat.id.desc())
        .first()
    )
    return download_total, save_total, last.timestamp if last is not None else None


def render_datastore_search_doi_page(query_doi):
    """
    Renders a DOI landing page for a datastore_search based query DOI.

    :param query_doi: the query DOI
    :returns: the rendered page
    """
    # currently we only deal with single resource query DOIs
    resource_id = query_doi.get_resource_ids()[0]
    rounded_version = query_doi.get_rounded_versions()[0]

    resource, package = get_resource_and_package(resource_id)
    # we ignore the saves count as it will always be 0 for a datastore_search DOI
    downloads, _saves, last_download_timestamp = get_stats(query_doi)
    context = {
        'query_doi': query_doi,
        'doi': query_doi.doi,
        'resource': resource,
        'package': package,
        # this is effectively an integration point with the ckanext-doi extension. If there is
        # demand we should open this up so that we can support other dois on packages extensions
        'package_doi': package['doi'] if package.get('doi_status', False) else None,
        'authors': get_authors([package]),
        'version': rounded_version,
        'reruns': generate_rerun_urls(
            resource, package, query_doi.query, rounded_version
        ),
        'downloads': downloads,
        'last_download_timestamp': last_download_timestamp,
    }

    return toolkit.render('query_dois/single_landing_page.html', context)


def get_package_and_resource_info(resource_ids):
    """
    Retrieve basic info about the packages and resources from the list of resource ids.

    :param resource_ids: a list of resource ids
    :returns: two dicts, one of package info and one of resource info
    """
    raction = partial(toolkit.get_action('resource_show'), {})
    paction = partial(toolkit.get_action('package_show'), {})

    packages = {}
    resources = {}
    for resource_id in resource_ids:
        resource = raction(dict(id=resource_id))
        package_id = resource['package_id']
        resources[resource_id] = {
            'name': resource['name'],
            'package_id': package_id,
        }
        if package_id not in packages:
            package = paction(dict(id=package_id))
            packages[package_id] = {
                'title': package['title'],
                'name': package['name'],
                'resource_ids': [],
            }
        packages[package_id]['resource_ids'].append(resource_id)

    return packages, resources


def create_current_slug(query_doi: QueryDOI) -> str:
    """
    Creates a slug for the given query DOI at the current version, this is done with a
    nav slug which has no version.

    :param query_doi: the QueryDOI
    :returns: a slug
    """
    slug_data_dict = {
        'query': query_doi.query,
        'query_version': query_doi.query_version,
        'resource_ids': query_doi.get_resource_ids(),
        'nav_slug': True,
    }
    current_slug = toolkit.get_action('vds_slug_create')({}, slug_data_dict)
    return current_slug['slug']


def render_multisearch_doi_page(query_doi: QueryDOI):
    """
    Renders a DOI landing page for a datastore_multisearch based query DOI.

    :param query_doi: the query DOI
    :returns: the rendered page
    """
    packages, resources = get_package_and_resource_info(query_doi.get_resource_ids())
    downloads, saves, last_download_timestamp = get_stats(query_doi)
    # order by count
    sorted_resource_counts = sorted(
        query_doi.resource_counts.items(), key=operator.itemgetter(1), reverse=True
    )
    current_slug = create_current_slug(query_doi)

    context = {
        'query_doi': query_doi,
        'resource_count': len(resources),
        'package_count': len(packages),
        'resources': resources,
        'packages': packages,
        'downloads': downloads,
        'saves': saves,
        'last_download_timestamp': last_download_timestamp,
        'sorted_resource_counts': sorted_resource_counts,
        'original_slug': query_doi.doi,
        'current_slug': current_slug,
    }
    return toolkit.render('query_dois/multisearch_landing_page.html', context)
