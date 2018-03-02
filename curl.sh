#!/bin/sh +x

##CURL
###https://curl.haxx.se/docs/manpage.html
~~~
fnQueryDeviceDetails()
{
  # $1: NMS IP address
  # $2: NMS NBAPI username
  # $3: NMS NBAPI password
  # $4: query string
  # $5: device EID
  postData="<soapenv:Envelope xmlns:soapenv=\"http://schemas.xmlsoap.org/soap/envelope/\"
    xmlns:sear=\"http://search.nbapi.xxx.com/\">
    <soapenv:Header/>
    <soapenv:Body>
      <sear:getDeviceDetails>
        <query>$4</query>
        <deviceIds>$5</deviceIds>
      </sear:getDeviceDetails>
    </soapenv:Body>
  </soapenv:Envelope>"
  

  var="$(curl -k -H "Content-Type: text/xml; charset=utf-8" --user "$2:$3"   \
       -H "SOAPAction: http://search.nbapi.xxx.com/getDeviceDetails" -d "$postData" \
       -1 -X POST https://$1/nbapi/search?wsdl 2>/dev/null)"

  printf "$var"
}
~~~

curl option cmd
 -k :  --insecure
    ```
        By default ,every SSL connection curl makes is verified to be secure,This option allows curl to proceed 
        and operate even for server connection otherwise considered insecure.

        The server connection is verified by making sure the server's certificate contains the right name and 
        verifies successfully the cert store.
    ```

-H : --header <header / @file>

-X : --requests <command>
    ```
        (HTTP)Specifies a custom request method to use when communicating with the HTTP server.

        Normally you dont need this option.All sort of GET, POST and PUT requests are rather invoked by 
        using dedicated command line option.
    ```

-d : --data <data>
    ```
        (HTTP)Sends the specified data in POST request to the HTTP server.in the same way that a browser does 
        when a user has filled in an HTML form and presses the submit button. This will cause curl to pass the
        data to the server using the content-typr application/x-www-form-urlencoded. 
    ```


