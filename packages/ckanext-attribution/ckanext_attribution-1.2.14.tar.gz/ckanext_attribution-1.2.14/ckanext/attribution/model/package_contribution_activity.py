#!/usr/bin/env python
# encoding: utf-8
#
# This file is part of ckanext-attribution
# Created by the Natural History Museum in London, UK

from ckan.model import DomainObject, meta, package_table
from ckan.model.types import make_uuid
from sqlalchemy import Column, ForeignKey, Table, UnicodeText

from ckanext.attribution.model.contribution_activity import contribution_activity_table

package_contribution_activity_table = Table(
    'package_contribution_activity',
    meta.metadata,
    Column('id', UnicodeText, primary_key=True, default=make_uuid),
    Column(
        'package_id',
        UnicodeText,
        ForeignKey('package.id', onupdate='CASCADE', ondelete='CASCADE'),
        nullable=False,
    ),
    Column(
        'contribution_activity_id',
        UnicodeText,
        ForeignKey('contribution_activity.id', onupdate='CASCADE', ondelete='CASCADE'),
        nullable=False,
        unique=True,
    ),
)


class PackageContributionActivity(DomainObject):
    """
    A link between a package and the contribution activity performed.
    """

    pass


def check_for_table():
    if package_table.exists() and contribution_activity_table.exists():
        package_contribution_activity_table.create(checkfirst=True)
