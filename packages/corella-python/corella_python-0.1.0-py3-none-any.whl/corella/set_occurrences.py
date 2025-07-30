from .add_eventID_occurrences import add_eventID_occurrences
from .add_unique_IDs import add_unique_IDs
from .check_occurrences import check_occurrences
from .common_functions import check_for_dataframe,set_data_workflow

def set_occurrences(dataframe=None,
                    occurrenceID=None,
                    catalogNumber=None,
                    recordNumber=None,
                    basisOfRecord=None,
                    sequential_id=False,
                    add_sequential_id='first',
                    composite_id=None,
                    sep='-',
                    random_id=False,
                    add_random_id='first',
                    occurrenceStatus=None,
                    errors=[],
                    add_eventID=False,
                    events=None,
                    eventType=None):
    """
    Checks for unique identifiers of each occurrence and how the occurrence was recorded.

    Parameters
    ----------
        dataframe: ``pandas.DataFrame``
            The ``pandas.DataFrame`` that contains your data to check
        occurrenceID: ``str`` or ``bool``
            Either a column name (``str``) or ``True`` (``bool``).  If a column name is 
            provided, the column will be renamed.  If ``True`` is provided, unique identifiers
            will be generated in the dataset.
            *Note*: Every occurrence should have an occurrenceID entry. Ideally, IDs should be 
            persistent to avoid being lost in future updates. They should also be unique, both within 
            the dataset, and (ideally) across all other datasets.
        catalogNumber: ``str`` or ``bool``
            Either a column name (``str``) or ``True`` (``bool``).  If a column name is 
            provided, the column will be renamed.  If ``True`` is provided, unique identifiers
            will be generated in the dataset.
        recordNumber: ``str`` or ``bool``
            Either a column name (``str``) or ``True`` (``bool``).  If a column name is 
            provided, the column will be renamed.  If ``True`` is provided, unique identifiers
            will be generated in the dataset.
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
        basisOfRecord: ``str``
            Either a column name (``str``) or a valid value for ``basisOfRecord`` to add to 
            the dataset.  For values of ``basisOfRecord``, it only accepts ``camelCase``, for consistency with field 
            ``"humanObservation"``, ``"machineObservation"``, ``"livingSpecimen"``, ``"preservedSpecimen"``, ``"fossilSpecimen"``, ``"materialCitation"``
        occurrenceStatus: ``str``
            Either a column name (``str``) or a valid value for ``occurrenceStatus`` to add to 
            the dataset.  Valid values are ``"present"`` or ``"absent"``
        errors: ``list``
            ONLY FOR DEBUGGING: existing list of errors.
        add_eventID: ``logic``
            Either a column name (``str``) or a valid value for ``occurrenceStatus`` to add to 
            the dataset.
        events: ``pd.DataFrame``
            Dataframe containing your events.
        eventType: ``str``
            Either a column name (``str``) or a valid value for ``eventType`` to add to 
            the dataset.

    Returns
    -------
        ``pandas.DataFrame`` with the updated data.

    Examples
    ----------
        `set_occurrences vignette <../../html/corella_user_guide/independent_observations/set_occurrences.html>`_
    """

    # check for dataframe
    check_for_dataframe(dataframe=dataframe,func='set_occurrences')
    
    # check for events for adding event ID
    if add_eventID:
        check_for_dataframe(dataframe=events,func='set_occurrences')

    # mapping of column names and variables
    mapping = {
        'occurrenceID': occurrenceID,
        'catalogNumber': catalogNumber,
        'recordNumber': recordNumber,
        'basisOfRecord': basisOfRecord,
        'occurrenceStatus': occurrenceStatus
    }

    # accepted data formats for each argument
    accepted_formats = {
        'occurrenceID': [str,bool],
        'catalogNumber': [str],
        'recordNumber': [str],
        'basisOfRecord': [str],
        'occurrenceStatus': [str]
    }

    # specify variables and values for set_data_workflow()
    variables = [occurrenceID,catalogNumber,recordNumber,basisOfRecord,occurrenceStatus]
    values = ['occurrenceID','catalogNumber','recordNumber','basisOfRecord','occurrenceStatus']

    # set column names and values specified by user
    dataframe = set_data_workflow(func='set_occurrences',dataframe=dataframe,mapping=mapping,variables=variables,
                                  values=values,accepted_formats=accepted_formats)
    
    # check if unique occurrence IDs need to be added
    if (type(occurrenceID) is bool) and occurrenceID: 
        dataframe = add_unique_IDs(column_name='occurrenceID',sequential_id=sequential_id,add_sequential_id=add_sequential_id,
                                   composite_id=composite_id,sep=sep,random_id=random_id,add_random_id=add_random_id,
                                   dataframe=dataframe)
        
    # check if we are adding eventID to occurrences
    if type(add_eventID) is bool and add_eventID:
        dataframe = add_eventID_occurrences(occurrences=dataframe,events=events,eventType=eventType)
        
    # check data
    errors = check_occurrences(dataframe=dataframe,errors=[])
    
    # return errors if there are any; otherwise, 
    if len(errors) > 0:
        raise ValueError("There are some errors in your data.  They are as follows:\n\n{}".format('\n'.join(errors)))
    return dataframe