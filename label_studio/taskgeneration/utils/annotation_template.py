def create_activity_annotation_template(timestamp_column_name,value_column_name):
    """
        Function that takes the names of the timestamp and value columns and creates an XML markup with it 
        for activity annotation

        :param timestamp_column_name
        :param value_column_name
        :return: String containing XML markup that can be used by LS. Default labels are run and walk. User can adjust this in LS
    """
    head = '<View><Header value="Activity annotation for $subject"/>'
    timeserieslabels = '<TimeSeriesLabels name="label" toName="ts"><Label value="Run"/><Label value="Walk"/></TimeSeriesLabels>'
    video = '<HyperText name="video" value="$video" inline="true"/>'
    timeseries =   f'<TimeSeries name="ts" value="$csv" valueType="url" timeColumn="{timestamp_column_name}" fixedScale="true"><Channel column="{value_column_name}"/></TimeSeries>'
    y_axis_documentation = '<Text name="text1" value="Be aware: The y-axis scales to maximum value in the file. This could result in peaks looking smaller or bigger than the same peak in other files."/>'
    tail = '</View>'


    return head + timeserieslabels + video + timeseries + y_axis_documentation + tail

