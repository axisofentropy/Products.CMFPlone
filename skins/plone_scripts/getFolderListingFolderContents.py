## Script (Python) "getFolderListingFolderContents"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=contentFilter=None,suppressHiddenFiles=1
##title=wrapper method around listFolderContents
##
from zLOG import LOG, WARNING
LOG('Plone Debug', WARNING, 'The getFolderListingFolderContents script is '
                            'deprecated, please use getFolderContents.')
return context.getFolderContents(contentFilter)