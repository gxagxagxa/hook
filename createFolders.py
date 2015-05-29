__author__ = 'Mac'

import os


os.environ['FTRACK_SERVER'] = 'http://192.168.9.200'
os.environ['FTRACK_APIKEY'] = 'b445309f-1c5d-40ac-b68b-3fdfb4f3ccb9'
os.environ['LOGNAME'] = 'andyguo'

# :coding: utf-8
# :copyright: Copyright (c) 2015 ftrack

import sys
import argparse
import logging

import ftrack
# import ftrack_connect.application


class MyAction(ftrack.Action):
    '''Describe your action here.'''

    #: Action identifier.
    identifier = 'com.phenom-films.createfolders'  # Unique identifier for your action.

    #: Action label.
    label = 'create folders'  # Action label which the user will see in the interface.

    def launch(self, event):
        '''Callback method for action.'''
        selection = event['data'].get('selection', [])
        self.logger.info(u'Launching action with selection {0}'.format(selection))

        # Validate selection and abort if not valid
        if not self.validateSelection(selection):
            self.logger.warning('Selection is not valid, aborting action')
            return

        # Implement your action logic here, return a UI or run some
        # code and return your result.
        #
        # If you are doing any heavy lifting, consider running offloading that
        # to a separate thread and returning quickly.
        #
        # To report back to the user you can utilize ftrack.createJob and then
        # update it's status and / or description.

        task = ftrack.Shot(id=selection[0]['entityId'])
        parents = task.getParents()
        for index, item in enumerate(parents):
            print(index, item)

        foldername = '/Users/mac/Desktop'
        for index in xrange(len(parents) - 1, -1, -1):
            foldername = os.path.join(foldername, parents[index].get('name'))
        # print foldername
        os.makedirs(foldername)


        pass

        return {
            'success': True,
            'message': 'createfolders completed successfully'
        }

    def discover(self, event):
        '''Return action config.'''
        selection = event['data'].get('selection', [])
        self.logger.info('%s', event)
        # self.logger.info(u'Discovering action with selection: {0}'.format(selection))




        # validate selection, and only return action if it is valid.
        if self.validateSelection(selection):
            return super(MyAction, self).discover(event)

    def validateSelection(self, selection):
        '''Return True if *selection* is valid'''
        # Replace with custom logic for validating selection.
        # For example check the length or entityType of items in selection.
        return True





def register(registry, **kw):
    '''Register action. Called when used as an event plugin.'''
    action = MyAction()
    action.register()


def main(arguments=None):
    '''Set up logging and register action.'''
    if arguments is None:
        arguments = []

    parser = argparse.ArgumentParser()
    # Allow setting of logging level from arguments.
    loggingLevels = {}
    for level in (
            logging.NOTSET, logging.DEBUG, logging.INFO, logging.WARNING,
            logging.ERROR, logging.CRITICAL
    ):
        loggingLevels[logging.getLevelName(level).lower()] = level

    parser.add_argument(
        '-v', '--verbosity',
        help='Set the logging output verbosity.',
        choices=loggingLevels.keys(),
        default='info'
    )
    namespace = parser.parse_args(arguments)

    # Set up basic logging
    logging.basicConfig(level=loggingLevels[namespace.verbosity])

    # Subscribe to action.
    ftrack.setup()
    action = MyAction()
    action.register()

    # Wait for events
    ftrack.EVENT_HUB.wait()


if __name__ == '__main__':
    raise SystemExit(main(sys.argv[1:]))




