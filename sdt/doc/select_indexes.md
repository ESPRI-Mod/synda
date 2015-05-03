# Select which ESGF index to use

* Edit sdt.conf

* Set default index

e.g.
    [index]
    default_index=esgf-node.ipsl.fr

This index is used in interactive mode.

* Set indexes list

e.g.
    [index]
    indexes=esgf-node.ipsl.fr,esgf-data.dkrz.de,esgf-index1.ceda.ac.uk,esg.ccs.ornl.gov

Those indexes are used in batch mode to reduce latence.

* Index list

    esg-datanode.jpl.nasa.gov
    esgf-node.ipsl.fr
    esgf-data.dkrz.de
    esgf-index1.ceda.ac.uk
    esg.ccs.ornl.gov
