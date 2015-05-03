# Download the nearest replica

To make Synda automaticaly select the nearest replica, set the following parameters in sdt/conf/sdt.conf

    [behaviour]
    nearest=true
    nearest_mode=geolocation

    [locale] 
    country=<your country>

Country value examples

    country=England
    country=Germany
    country=France
    ...

To show available replica for a file, you can run the command below

    synda search cmip5.output1.CNRM-CERFACS.CNRM-CM5.historicalMisc.day.ocean.day.r1i1p1.v20120619.tossq_day_CNRM-CM5_historicalMisc_r1i1p1_19300101-19391231.nc -r

To test if the nearest replica is correctly selected, you can run the command below

    synda dump cmip5.output1.CNRM-CERFACS.CNRM-CM5.historicalMisc.day.ocean.day.r1i1p1.v20120619.tossq_day_CNRM-CM5_historicalMisc_r1i1p1_19300101-19391231.nc -F indent | grep data_node

It will show which replica has been selected.
 
### Examples

If you are located in England *AND* there is a replica available in England

output of the last command should looks like

    esgf-data1.ceda.ac.uk

If you are located in Germany *AND* there is a replica available in Germany

output of the last command should looks like

    wdcc-esgf.dkrz.de

etc..
