# OTU_predictor

`OTU_predictor` uses a trained `RandomForestClassifier` ML model to predict 'real' OTU presence from ancient metagenomic samples (although it's use is not limited to ancient samples). The training dataset consists of 200 simulated populations generated through [InSilicoSeq](https://github.com/HadrienG/InSilicoSeq) and deaminated using [gargammel](https://github.com/grenaud/gargammel). Each population contains between 5 and 20 microbial species with know, variable abundance. `OTU_predictor` uses input files generated in [centrifgure](https://ccb.jhu.edu/software/centrifuge/), specifically `centrifugeReport.txt` files.

## Install package

`OTU_predictor` is currently running on `python 3.11`. It may run on earlier python versions also, but this has not been extensively tested. The easiest way to install `OTU_predictor` is using `pip`. Either of the following commands will do this:

```bash
pip install OTU-predictor
```
or

```bash
pip install git+https://github.com/DrATedder/OTU_predictor.git
```
## Basic Usage

### 1. Converting your data

`OTU_predictor` works with `centrifugeReport.txt` files. Before you can run the model prediction step, some minor format teaks are required (see example output below). This can be done in the following way:

```python

import OTU_predictor

centrifugeReport = "/path/to/your/file_centrifugeReport.txt"
OTU_predictor.convert_file(centrifugeReport)
```

If this step is successful, you will see a message similar to the one below:

```python
'Data file /path/to/your/file_centrifugeReport_data.txt created'
```

The output data format should look something like this:

name|taxID|taxRank|genomeSize|numReads|numUniqueReads|abundance|genus|presence|sim_abundance
 --- | --- | --- | --- | --- |--- | --- | --- | --- | --- |
Bacteria|2|superkingdom|0|127|103|0.00026298841815572643|NA|0|0
Azorhizobium|6|genus|5369772|1|0|2.070774946108082e-06|Azorhizobium|0|0
Azorhizobium caulinodans|7|species|5369772|3|0|6.212324838324246e-06|Azorhizobium|0|0
Buchnera aphidicola|9|species|602805|3|1|6.212324838324246e-06|Buchnera|0|0
Cellulomonas gilvus|11|species|3526441|15|0|3.106162419162123e-05|Cellulomonas|0|0
Phenylobacterium|20|genus|4379231|1|0|2.070774946108082e-06|Phenylobacterium|0|0
Shewanella|22|genus|5140018|10|1|2.0707749461080822e-05|Shewanella|0|0
Shewanella putrefaciens|24|species|4749735|2|1|4.141549892216164e-06|Shewanella|0|0
Myxococcales|29|order|9638245|171|0|0.00035410251578448204|NA|0|0
Myxococcaceae|31|family|9636120|9|0|1.863697451497274e-05|NA|0|0
Myxococcus|32|genus|9487953|10|0|2.0707749461080822e-05|Myxococcus|0|0
Myxococcus xanthus|34|species|9139763|47|10|9.732642246707986e-05|Myxococcus|0|0
Myxococcus macrosporus|35|species|8973512|20|8|4.1415498922161644e-05|Myxococcus|0|0
Archangiaceae|39|family|10085598|11|0|2.2778524407188902e-05|NA|0|0
Stigmatella|40|genus|10260756|2|0|4.141549892216164e-06|Stigmatella|0|0
Stigmatella aurantiaca|41|species|10260756|1|0|2.070774946108082e-06|Stigmatella|0|0
Cystobacter|42|genus|0|1|0|2.070774946108082e-06|Cystobacter|0|0

**Note.** You will notice the addition of three new columns. these are variables used by the model during training, and while it is essential for them to be included for the file to be valid, they are not interpreted as part of the prediction step. It is also worth pointing out that the 'tab-delimitation' is replaced by 'comma-delimitation'.

### 2. Making predictions

The `make_predictions()` function uses your data file and the trained model which packages with this distribution. It is possible to create your own model if this is preferable though. The basic steps to make predictions are as follows:

```python
converted_data = "/path/to/your/file_centrifugeReport_data.txt"

OTU_predictor.make_predictions(converted_data)

```
The output will be a list (of dictionaries) similar to the one shown below:

```python
[{'Species': 'Neisseria mucosa', 'TaxID': 488, 'Prediction': 1, 'Certainty': 0.68},
{'Species': 'Streptococcus sanguinis', 'TaxID': 1305, 'Prediction': 1, 'Certainty': 0.72},
{'Species': 'Actinomyces sp. oral taxon 414', 'TaxID': 712122, 'Prediction': 1, 'Certainty': 0.97},
{'Species': 'Olsenella sp. oral taxon 807', 'TaxID': 712411, 'Prediction': 1, 'Certainty': 0.88},
{'Species': 'Anaerolineaceae bacterium oral taxon 439', 'TaxID': 1889813, 'Prediction': 1, 'Certainty': 0.87},
{'Species': 'Desulfobulbus oralis', 'TaxID': 1986146, 'Prediction': 1, 'Certainty': 0.84}]
```

**Note.** As you can see from the output list, OTU (`species` - although it can be at any taxonomic level determined by centrifuge) and `taxID` are given, along with a `certainty` score. These scores will be between 0 and 1, with higher scores indicating increased certainty. `Prediction: 1` is OTU presence in the sample. The model also determines (but does not show) OTU absence (`Prediction: 0`). 

Users should choose a `certainty` score that fits their experimental purpose.
