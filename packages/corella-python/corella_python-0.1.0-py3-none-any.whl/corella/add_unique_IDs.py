import uuid
from .common_functions import check_for_dataframe

def add_unique_IDs(dataframe=None,
                   column_name="occurrenceID",
                   sequential_id=False,
                   add_sequential_id='first',
                   add_random_id='first',
                   composite_id=None,
                   sep='-',
                   random_id=False):
        """
        Function that automatically adds unique IDs (in the form of uuids) to each of your occurrences.

        Parameters
        ----------
            dataframe : ``pandas Dataframe``
                ``dataframe`` containing your data.
            column_name : ``str``
                String containing name of column you want to add.  Default is ``occurrenceID``
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
            

        Returns
        -------
            ``None``

        Examples
        --------

        .. prompt:: python

            import galaxias
            import pandas as pd
            data = pd.read_csv("occurrences_dwc.csv")
            my_dwca = galaxias.dwca(occurrences=data)
            my_dwca.add_unique_occurrence_IDs()
            my_dwca.occurrences

        .. program-output:: python -c "import galaxias;import pandas as pd;pd.set_option('display.max_columns', None);pd.set_option('display.expand_frame_repr', False);pd.set_option('max_colwidth', None);data = pd.read_csv(\\\"galaxias_user_guide/occurrences_dwc.csv\\\");my_dwca = galaxias.dwca(occurrences=data);my_dwca.add_unique_occurrence_IDs();print(my_dwca.occurrences)"
        """
        # check for empty dataframe
        check_for_dataframe(dataframe=dataframe,func='add_unique_IDs')

        # declare valid ID column names
        valid_id_names = ["occurrenceID","catalogNumber","recordNumber","eventID"]
        
        # check if column name is in valid_id_names; if it is, add column.  If not, raise ValueError.
        if column_name in valid_id_names:
            if random_id and not sequential_id and composite_id is None:
                uuids = [None for i in range(dataframe.shape[0])]
                for i in range(dataframe.shape[0]):
                    uuids[i] = str(uuid.uuid4())
                dataframe.insert(0,column_name,uuids)
                return dataframe
            elif sequential_id and composite_id is None:
                ids = [str(x) for x in range(dataframe.shape[0])]
                dataframe.insert(0,column_name,ids)
                return dataframe
            elif composite_id is not None:
                if sequential_id:
                    ids = [str(x) for x in range(dataframe.shape[0])]
                    if add_sequential_id == 'first':
                        if type(composite_id) is str:
                            dataframe.insert(0,column_name,[item + sep for item in ids] + dataframe[composite_id])
                        else:
                            dataframe.insert(0,column_name,[item + sep for item in ids] + dataframe[composite_id].agg(sep.join, axis=1))
                    elif add_sequential_id == 'last':
                        if type(composite_id) is str:
                            dataframe.insert(0,column_name,dataframe[composite_id] + [sep + item for item in ids])
                        else:
                            dataframe.insert(0,column_name,dataframe[composite_id].agg(sep.join, axis=1) + [sep + item for item in ids])
                    else:
                        raise ValueError("Please provide only \'first\' and \'last\' as arguments for add_sequential_id.")
                    return dataframe
                elif random_id:
                    ids = [str(uuid.uuid4()) for x in range(dataframe.shape[0])]
                    if add_random_id == 'first':
                        if type(composite_id) is str:
                            dataframe.insert(0,column_name,[item + sep for item in ids] + dataframe[composite_id])
                        else:
                            dataframe.insert(0,column_name,[item + sep for item in ids] + dataframe[composite_id].agg(sep.join, axis=1))
                    elif add_random_id == 'last':
                        if type(composite_id) is str:
                            dataframe.insert(0,column_name,dataframe[composite_id] + [sep + item for item in ids])
                        else:
                            dataframe.insert(0,column_name,dataframe[composite_id].agg(sep.join, axis=1) + [sep + item for item in ids])
                    else:
                        raise ValueError("Please provide only \'first\' and \'last\' as arguments for add_sequential_id.")
                    return dataframe
                else:
                    if type(composite_id) is list:
                        dataframe.insert(0,column_name,dataframe[composite_id].agg(sep.join, axis=1))
                    else:
                        raise ValueError("Please provide more than one column names for composite id.  Or, add a sequential or random ID")
                    return dataframe
            else:
                if not random_id and not sequential_id and composite_id is None:
                    raise ValueError("Please specify whether or not you want a random ID, sequential ID or composite ID.")
                else:
                    print("random_id={}".format(random_id))
                    print("sequential_id={}".format(sequential_id))
                    print("composite_id={}".format(composite_id))
        else:
            raise ValueError("Please provide one of the following column names: \n\n{}".format(valid_id_names))