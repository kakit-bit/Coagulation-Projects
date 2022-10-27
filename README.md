<h1> INTRODUCTION

<h2>This Python script automates the set-up and preparation of a laboratory based test called the Nijmegen Bethesda Assay. This assay determines whether or not a patient has a specific inhibitor toward a clotting factor protein.
<br></br>
<h2>Script accomodates the set-up of the Nijmegen assay set-up as outlined by the standardized operating procedures at St. Michael's Hospital. 
<br></br>
<h1>Reagent Calculator
<h2>Script accepts user input for number of samples to run. For each number of sample, accepts user input for demographics. From demographic entry, summation of dilutions for resource count. Calculates resources required then shows how much assay specific reagent to prepare.
<br></br>
<h2>Useful as the assay is quite resource expensive.
<br></br>
<h1>Nijmegen Calculator
<br></br>
<h2>Script unpacks each patient and dilutions allowing for result entry from the analyzer. For each dilution, function mathematically converts entered value into residual activity.
<br></br>
<h2>From residual activity, presence of inhibitor is determined. If an inhibitor is present, script will search the array to find closest to 50% activit yand return the dilution it was found at with corrected Bethesda Unit.
<br></br>
<h2>Openpyxl module and templated Excel sheet required for script to output information and save as independent file.
<br></br>
<h2>Features error checking.