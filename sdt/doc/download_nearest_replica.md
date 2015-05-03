If you set the following parameters in sdt.conf, it should work.


		- set country 
If you set the following parameters in sdt.conf, it should work.

[behaviour]
nearest=true
nearest_mode=geolocation

[locale] 

country=England



To test it, you can run the command below

synda dump cmip5.output1.CNRM-CERFACS.CNRM-CM5.historicalMisc.day.ocean.day.r1i1p1.v20120619.tossq_day_CNRM-CM5_historicalMisc_r1i1p1_19300101-19391231.nc -F indent | grep data_node


It should return the nearest data_node, i.e. esgf-data1.ceda.ac.uk

