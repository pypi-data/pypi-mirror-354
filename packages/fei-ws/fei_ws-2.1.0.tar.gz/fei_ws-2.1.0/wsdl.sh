#!/bin/sh

base_url='https://data.fei.org/_vti_bin'
version='1_2'


curl $base_url/Authentication.asmx?WSDL >| fei_ws/wsdl/auth.wsdl
curl $base_url/FEI/OrganizerWS_$version.asmx?WSDL >| fei_ws/wsdl/org_$version.wsdl
curl $base_url/FEI/CommonWS.asmx?WSDL >| fei_ws/wsdl/common.wsdl
