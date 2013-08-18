#!/usr/bin/env python
# vim: ai ts=4 sts=4 et sw=4 fileencoding=utf-8
# maintainer: katembu

from forms.CaseXMLInterface import CaseXMLInterface


class PregnancyForm(CaseXMLInterface):

    ''' Pregnancy Form'''

    template_name = 'pregnancy.xml'
    template_dict = {}
