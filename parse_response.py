import json

if __name__=='__main__':
    response = [{"type":"text","text":"Great a new locker ticket has been opened:{\"result\":{\"sys_id\":\"d44375183b204750828d4fd1d9f3e6c2\",\"number\":\"GWS0868361\",\"$$uiNotification\":[{\"type\":\"info\",\"message\":\"This ticket was opened for your request<br />You will be contacted if further information is required.<br />\"}],\"parent_id\":null,\"record\":\"api/now/table/x_redha_gws_table/d44375183b204750828d4fd1d9f3e6c2\",\"redirect_portal_url\":\"\",\"parent_table\":\"task\",\"redirect_url\":\"x_redha_gws_table.do?sys_id=d44375183b204750828d4fd1d9f3e6c2&sysparm_view=\",\"table\":\"x_redha_gws_table\",\"redirect_to\":\"generated_record\"}}"}]

    prefix = "Great a new locker ticket has been opened:"
    nested_json_str = response[0]["text"].replace(prefix, "")

    # Parse the nested JSON
    nested_data = json.loads(nested_json_str)

    # Extract the values
    number = nested_data["result"]["number"]
    sys_id = nested_data["result"]["sys_id"]

    print("Number:", number)
    print("Sys ID:", sys_id)


    request_url = f"https://redhat.service-now.com/help?id=rh_ticket&table=x_redha_gws_table&sys_id={sys_id}"

    print("URL", request_url)






