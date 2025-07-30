import pandas as pd
from .check_events import check_events
from .common_functions import check_for_dataframe,set_data_workflow
from .generate_eventID_parentEventID import generate_eventID_parentEventID

def set_events(dataframe=None,
               eventID=None,
               parentEventID=None,
               eventType=None,
               Event=None,
               samplingProtocol=None,
               event_hierarchy=None,
               sequential_id=False,
               add_sequential_id='first',
               add_random_id='first',
               composite_id=None,
               sep='-',
               random_id=False):
    """
    Identify or format columns that contain information about an Event. An "Event" in Darwin Core Standard refers to an action that occurs at a place and time. Examples include:

    - A specimen collecting event
    - A survey or sampling event
    - A camera trap image capture
    - A marine trawl
    - A camera trap deployment event
    - A camera trap burst image event (with many images for one observation)

    Parameters
    ----------
        dataframe: ``pandas.DataFrame``
            The ``pandas.DataFrame`` that contains your data to check
        eventID: ``str``, ``logical``
            A column name (``str``) that contains a unique identifier for your event.  Can also be set 
            to ``True`` to generate values.  Parameters for these values can be specified with the arguments 
            ``sequential_id``, ``add_sequential_id``, ``composite_id``, ``sep`` and ``random_id``
        sequential_id: ``logical``
            Create sequential IDs and/or add sequential ids to composite ID.  Default is ``False``.
        add_sequential_id: ``str``
            Determine where to add sequential id in composite id.  Values are ``first`` and ``last``.  Default is ``first``.
        composite_id: ``str``, ``list``
            ``str`` or ``list`` containing columns to create composite IDs.  Can be combined with sequential ID.
        sep: ``char``
            Separation character for composite IDs.  Default is ``-``.
        random_id: ``logical``
            Create a random ID using the ``uuid`` package.  Default is ``False``.
        add_random_id: ``str``
            Determine where to add sequential id in random id.  Values are ``first`` and ``last``.  Default is ``first``.
        parentEventID: ``str``
            A column name (``str``) that contains a unique ID belonging to an event below 
            it in the event hierarchy.
        eventType: ``str`` 
            A column name (``str``) or a ``str`` denoting what type of event you have.
        Event: ``str`` 
            A column name (``str``) or a ``str`` denoting the name of the event.
        samplingProtocol: ``str`` or 
            Either a column name (``str``) or a ``str`` denoting how you collected the data, 
            i.e. "Human Observation".
        event_hierarchy: ``dict``
            A dictionary containing a hierarchy of all events so they can be linked.  For example, 
            if you have a set of observations that were taken at a particular site, you can use the 
            dict {1: "Site Visit", 2: "Sample", 3: "Observation"}.

    Returns
    -------
        ``pandas.DataFrame`` with the updated data.

    Examples
    ----------
        `set_events vignette <../../html/corella_user_guide/longitudinal_studies/set_events.html>`_
    """
    
    # first, check for data frame
    check_for_dataframe(dataframe=dataframe,func='set_events')

    # mapping of column names and variables
    mapping = {
        'eventID': eventID,
        'parentEventID': parentEventID, 
        'eventType': eventType,
        'Event': Event,
        'samplingProtocol': samplingProtocol
    }

    # accepted data formats for each argument
    accepted_formats = {
        'eventID': [str,bool],
        'parentEventID': [str,bool], 
        'eventType': [str],
        'Event': [str],
        'samplingProtocol': [str]
    }

    # specify variables and values for set_data_workflow()
    variables = [eventID,parentEventID,eventType,Event,samplingProtocol]
    values = ['eventID','parentEventID','eventType','Event','samplingProtocol']

    # set column names and values specified by user
    dataframe = set_data_workflow(func='set_events',dataframe=dataframe,mapping=mapping,variables=variables,
                                  values=values,accepted_formats=accepted_formats)

    # check for event_hierarchy
    if type(eventID) is bool:
        if parentEventID is None:
            print("parentEventID has not been provided, but will automatically be generated.")
            dataframe = generate_eventID_parentEventID(dataframe=dataframe,event_hierarchy=event_hierarchy,
                                                       sequential_id=sequential_id,
                                                       add_sequential_id=add_sequential_id,
                                                       add_random_id=add_random_id,
                                                       sep=sep,random_id=random_id,
                                                       composite_id=composite_id)
        elif parentEventID in mapping:
            raise ValueError("a parentEventID column has been provided, but eventID has not. Please provide your eventID column.")
    elif not set(dataframe.columns).issuperset({'eventID','parentEventID'}) and event_hierarchy is None:
        raise ValueError("Please provide column names for eventID and parentEventID.  Or, provide an event_hierarchy dictionary for automatic ID generation.")
    elif event_hierarchy is not None and not set(dataframe.columns).issuperset({'eventID','parentEventID'}):
        dataframe=generate_eventID_parentEventID(dataframe=dataframe,event_hierarchy=event_hierarchy,
                                                 sequential_id=sequential_id,
                                                 add_sequential_id=add_sequential_id,
                                                 add_random_id=add_random_id,
                                                 composite_id=composite_id,sep=sep,
                                                 random_id=random_id)
    else:
        pass

    # check for errors
    errors = check_events(dataframe=dataframe,errors=[])
    
    # return errors if there are any; otherwise, return dataframe
    if len(errors) > 0:
        raise ValueError("There are some errors in your data.  They are as follows:\n\n{}".format('\n'.join(errors)))
    return dataframe