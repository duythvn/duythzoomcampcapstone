if 'transformer' not in globals():
    from mage_ai.data_preparation.decorators import transformer
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test
import pandas as pd

@transformer
def transform(data, *args, **kwargs):
    """
    transform main df loaded from data lake if need to
    """
    #convert
    #print(data['unnamed:_0'])
    #df=data.drop(columns=['unnamed:_0'])
    df=data
    print(df.columns)

    #standardise column names by doing camel case conversion ( "columnName" would be transformed to "column_Name".).
    #also replace spaces with underscores and convert to lowercases

    df.columns = (df.columns
        .str.replace('(?<=[a-z])(?=[A-Z])| ', '_', regex=True)                
        .str.lower()
        )
    print(df.columns)
    # Assuming 'df' is your DataFrame with the given data
    df['first_response_time'] = pd.to_datetime(df['first_response_time'], errors='coerce')
    df['time_to_resolution'] = pd.to_datetime(df['time_to_resolution'], errors='coerce')

    # Function to calculate hours between two datetime values
    def calculate_hours(row):
        if pd.notna(row['time_to_resolution']) and pd.notna(row['first_response_time']):
            return (row['time_to_resolution'] - row['first_response_time']).total_seconds() / 3600
        else:
            return None

    # Apply the function to create the new column
    df['hours_to_resolve'] = df.apply(calculate_hours, axis=1)
    
    # # remove any value in hours_to_resolve which < 0 hours to empty and set status = "invalid"
    # df.loc[df['hours_to_resolve'] < 0, 'resolution_sla_status'] = 'invalid'
    # df.loc[df['hours_to_resolve'] < 0, 'hours_to_resolve'] = ''
    
    


    # Convert 'time_to_resolution' to numeric if not empty ,  errors='coerce' will yield a NaN  when there is error in converting 
    df.loc[df['time_to_resolution'].notna(), 'time_to_resolution'] = pd.to_numeric(df['time_to_resolution'], errors='coerce')

    # Mark rows with 'time_to_resolution' < 0 as 'invalid'   'time_to_resolution' > 0 as 'valid',  otherwise, mark it as 'NA'
    df.loc[(df['time_to_resolution'] < 0), 'resolution_sla_status'] = 'invalid'
    df.loc[(df['time_to_resolution'] < 0), 'time_to_resolution'] = ''

    df.loc[df['hours_to_resolve'] > 0, 'resolution_sla_status'] = 'valid'
    df.loc[df['time_to_resolution'].isna(), 'resolution_sla_status'] = 'na'    

    # Display the resulting DataFrame
    
    print(df)
    #df.to_csv("./testoutput.csv",index=False)

    return df


@test
def test_output(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert output is not None, 'The output is undefined'
