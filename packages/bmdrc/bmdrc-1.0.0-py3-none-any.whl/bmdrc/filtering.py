import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

__author__ = "David Degnan"

def make_plate_groups(self):
    '''
    Support function for the filter modules. Assign groups based on the chemical, concentration, plate, and endpoint. This step should be completed after all pre-processing steps are finished. 
    '''

    # If the data is BinaryClass where plate and well information is available, do the following
    if hasattr(self, "value"):
       
        # Keep just the required columns 
        pre_plate_groups = self.df[[self.chemical, self.concentration, self.plate, self.endpoint, self.value]]

        # Make a grouped data frame
        grouped_plate_groups = pre_plate_groups.groupby(by = [self.chemical, self.concentration, self.plate, self.endpoint], as_index = False)
            
        # Get the number of samples per group
        num_tot_samples = grouped_plate_groups.size().rename(columns = {"size": "bmdrc.num.tot"})

        # Get the number of non-na samples per groups
        num_nonna = grouped_plate_groups.count().rename(columns = {"value": "bmdrc.num.nonna"})

        # Get the number affected
        num_affected = grouped_plate_groups.sum().rename(columns = {"value": "bmdrc.num.affected"})

        # Merge to create missingness dataframe
        self.plate_groups = pd.merge(pd.merge(num_tot_samples, num_nonna), num_affected)

    # Else the data is SimplifiedClass
    else:

        # Keep just the required columns 
        self.plate_groups = self.df[[self.chemical, self.concentration, self.plate, self.endpoint, self.response]]

    # Create IDs of chemical.id, plate.id, and endpoint in plate_groups 
    self.plate_groups["bmdrc.Plate.ID"] = self.plate_groups[self.chemical].astype(str) + " " + \
                                            self.plate_groups[self.plate].astype(str) + " " + \
                                            self.plate_groups[self.endpoint].astype(str)
    
    # Create endpoint groups 
    self.plate_groups["bmdrc.Endpoint.ID"] = self.plate_groups[self.chemical].astype(str) + " " + \
                                            self.plate_groups[self.endpoint].astype(str) 

    # Add a filtered status
    self.plate_groups["bmdrc.filter"] = "Keep"

    # Add a filtered reason status 
    self.plate_groups["bmdrc.filter.reason"] = ""
        
def __negative_control_plot(neg_control_df):
    '''
    Support function for the filter modules. 
    Return the negative control diagnostic plot. 
    '''

    fig = plt.figure(figsize = (10, 5))

    colors = {'Keep':'steelblue', 'Remove':'firebrick'}
    color_choices = neg_control_df["Filter"].apply(lambda x: colors[x])
    labels = list(colors.keys())
    handles = [plt.Rectangle((0,0),1,1, color=colors[label]) for label in labels]

    plt.bar(x = [x for x in range(len(neg_control_df))], height = neg_control_df["Count"], 
            edgecolor = "black", tick_label = np.round(neg_control_df["Response"], 4),
            color = color_choices, label = neg_control_df["Filter"])
    plt.title("Counts of proportional responses per plate, endpoint, and chemical group")
    plt.xlabel("Proportional response in negative controls")
    plt.ylabel("Count")
    plt.legend(handles, labels)

    return(fig)

def negative_control(self, percentage: float, apply: bool, diagnostic_plot: bool):
    '''
    Filter to remove plates with unusually high expression in the controls. 

    Parameters
    -----------
    percentage
        A float between 0 and 100 indicating the percentage of phenotypic expression in the controls that is permissable. Default is 50. 
    
    apply
        A boolean to determine whether the filter should be applied. Default is False. 
    
    diagnostic_plot
        A boolean to determine whether to make a diagnostic plot if apply is False. Default is False.
    '''

    ##################
    ## CHECK INPUTS ##
    ##################
    
    # Check that percentage is in the right range 
    if percentage < 0 or percentage > 100:
        print("percentage must be between 0 and 100.")
        percentage = 50
    
    # Let the user know they picked a small value, but that it is acceptable. 
    if (percentage < 1):
        print("percentage should range from 0-100, as in 0-100%. This value will be a very small percentage.")

    ##############################
    ## MAKE GROUPS IF NECESSARY ##
    ##############################

    try:
        self.plate_groups
    except AttributeError:
        make_plate_groups(self)
    
    ###############################
    ## CREATE DIAGNOSTIC SUMMARY ##
    ###############################

    # Extract negative controls 
    NegControls = self.plate_groups[self.plate_groups[self.concentration] == 0].copy()

    # Calculate responses in negative controls
    NegControlRes = pd.DataFrame((NegControls["bmdrc.num.affected"] / NegControls["bmdrc.num.nonna"])).value_counts().rename_axis("Response").reset_index().rename(columns = {"count":"Count"}).sort_values(by = ["Response"]).reset_index(drop=True)
    
    # Multiply Response by 100 to make it a percentage
    NegControlRes["Response"] = NegControlRes["Response"] * 100

    # Set all values to be kept 
    NegControlRes["Filter"] = "Keep"

    # Determine what values will be removed
    NegControlRes.loc[NegControlRes["Response"] >= percentage, "Filter"] = "Remove"

    # Always make the backend data frame 
    self.filter_negative_control_df = NegControlRes
    self.filter_negative_control_thresh = percentage
    self.filter_negative_control_plot = __negative_control_plot(NegControlRes)

    #######################
    ## RETURN DIAGNOSTIC ##
    #######################

    if apply == False:
        if diagnostic_plot == False:
            plt.close(self.filter_negative_control_plot)
    
    #############################
    ## OTHERWISE, APPLY FILTER ##
    #############################

    else:

        # Get plate IDs
        NegControls["Response"] = NegControls["bmdrc.num.affected"] / NegControls["bmdrc.num.nonna"]        
        Plates = NegControls[NegControls["Response"] >= (percentage/100)]["bmdrc.Plate.ID"].tolist()

        # Apply filter
        self.plate_groups.loc[self.plate_groups["bmdrc.Plate.ID"].isin(Plates), "bmdrc.filter"] = "Remove"
        self.plate_groups.loc[self.plate_groups["bmdrc.Plate.ID"].isin(Plates), "bmdrc.filter.reason"] =  \
            self.plate_groups.loc[self.plate_groups["bmdrc.Plate.ID"].isin(Plates), "bmdrc.filter.reason"] + " negative_control_filter"


def __min_concentration_plot(min_concentration_df):
    '''
    Support function for the filter modules. 
    Returns the minimum concentration diagnostic plot. 
    '''

    fig = plt.figure(figsize = (10, 5))

    colors = {'Keep':'steelblue', 'Remove':'firebrick'}
    color_choices = min_concentration_df["Filter"].apply(lambda x: colors[x])
    labels = list(colors.keys())
    handles = [plt.Rectangle((0,0),1,1, color=colors[label]) for label in labels]

    # Turn off auto-display of plots
    plt.ioff()

    plt.bar(x = [x for x in range(len(min_concentration_df))], height = min_concentration_df["Count"], 
            edgecolor = "black", tick_label = min_concentration_df["NumConc"],
            color = color_choices, label = min_concentration_df["Filter"])
    plt.title("Counts of the number of concentrations per chemical and endpoint")
    plt.xlabel("Number of Concentrations")
    plt.ylabel("Total")
    plt.legend(handles, labels)

    return(fig)

def min_concentration(self, count: int, apply: bool, diagnostic_plot: bool): 
    '''
    Filter to remove endpoints without enough concentration measurements. This count does not include
    the baseline/control measurement of a concentration of 0. 

    Parameters
    ----------
    count
        An integer indicating the minimum number of concentrations an endpoint and chemical combination needs. Default is 3. 

    apply
        A boolean to indicate whether the filter should be applied. Default is False. 

    diagnostic_plot
        A boolean to determine whether to make a diagnostic plot if apply is False. Default is False.
    '''

    ##################
    ## CHECK INPUTS ##
    ##################
    
    # Count must be 1 or larger
    if count < 1:
        print("count must be at least 1.")
        count = 1

    ##############################
    ## MAKE GROUPS IF NECESSARY ##
    ##############################

    try:
        self.plate_groups
    except AttributeError:
        make_plate_groups(self)

    ###############################
    ## CREATE DIAGNOSTIC SUMMARY ##
    ###############################

    # Pull plate groups and remove all 0's 
    PlateGroupsNonZero = self.plate_groups[self.plate_groups[self.concentration] != 0]

    # Get a count per concentration group
    ConcCount = PlateGroupsNonZero.loc[PlateGroupsNonZero["bmdrc.filter"] == "Keep", ["bmdrc.Endpoint.ID", self.concentration]].groupby("bmdrc.Endpoint.ID").nunique().reset_index().rename(columns = {self.concentration:"NumConc"})

    # Get summary counts of counts
    ConcCountSum = ConcCount["NumConc"].value_counts().reset_index().rename(columns = {"count":"Count"}).sort_values(["NumConc"])

    # Keep all by default
    ConcCountSum["Filter"] = "Keep"

    # Apply filter threshold
    ConcCountSum.loc[ConcCountSum["NumConc"] < count, "Filter"] = "Remove"

    # Add summary filter to object
    self.filter_min_concentration_df = ConcCountSum.sort_values("NumConc", ascending = False).reset_index(drop = True)
    self.filter_min_concentration_thresh = count
    self.filter_min_concentration_plot = __min_concentration_plot(ConcCountSum)

    #######################
    ## RETURN DIAGNOSTIC ##
    #######################

    if apply == False:
        if diagnostic_plot == False:
            plt.close(self.filter_min_concentration_plot)

    #############################
    ## OTHERWISE, APPLY FILTER ##
    #############################

    else:
        
        # Get list of endpoints to remove
        EndpointRemoval = ConcCount.loc[ConcCount["NumConc"] < count, "bmdrc.Endpoint.ID"].tolist()

        self.plate_groups.loc[self.plate_groups["bmdrc.Endpoint.ID"].isin(EndpointRemoval), "bmdrc.filter"] = "Remove"
        self.plate_groups.loc[self.plate_groups["bmdrc.Endpoint.ID"].isin(EndpointRemoval), "bmdrc.filter.reason"] = \
            self.plate_groups.loc[self.plate_groups["bmdrc.Endpoint.ID"].isin(EndpointRemoval), "bmdrc.filter.reason"] + " min_concentration_filter"


def __correlation_score_plot(correlation_score, threshold):
    '''
    Support function for the filter modules. 
    Returns the distribution of correlation scores. 
    '''

    fig = plt.figure(figsize = (10, 5))

    # Fix bin sizes 
    the_bins = [x/100 for x in range(-100, 105, 5)]

    # Get counts a bin sizes
    k_counts, k_bins = np.histogram(correlation_score.loc[correlation_score["Filter"] == "Keep", "Spearman"], bins = the_bins)
    r_counts, r_bins = np.histogram(correlation_score.loc[correlation_score["Filter"] == "Remove", "Spearman"], bins = the_bins)

    # Turn off auto-display of plots
    plt.ioff()

    # Make plot
    plt.hist(k_bins[:-1], k_bins, weights = k_counts, color = "steelblue", label = "Keep", ec = "k")
    plt.hist(r_bins[:-1], r_bins, weights = r_counts, color = "firebrick", label = "Remove", ec = "k")

    # Create legend
    handles = [plt.Rectangle((0,0),1,1, color=c, ec = "k") for c in ["firebrick", "steelblue"]]
    labels= ["Remove", "Keep"]
    plt.legend(handles, labels)

    # Label axes
    plt.title("Counts of the spearman correlations for endpoint and chemical combinations")
    plt.xlabel("Spearman Correlation")  
    plt.ylabel("Count")

    # Add line at correlation
    plt.axvline(x = threshold, color = "red")

    return fig

def correlation_score(self, score: float, apply: bool, diagnostic_plot: bool): 
    '''
    Filter to remove endpoints with low correlation score thresholds.

    Parameters
    ----------
    score 
        A threshold for the correlation score as a float (ranging from -1 to 1). 

    apply
        A boolean to determine whether the filter is applied to the data. Default is False. 

    diagnostic_plot
        A boolean to determine whether to make a diagnostic plot if apply is False. Default is False.
    
    '''

    ##################
    ## CHECK INPUTS ##
    ##################
    
    # Score must be greater than -1 or less than 1
    if score < -1:
        score = -1
    elif score > 1:
        score = 1

    ##############################
    ## MAKE GROUPS IF NECESSARY ##
    ##############################

    try:
        self.plate_groups
    except AttributeError:
        make_plate_groups(self)

    ###############################
    ## CREATE DIAGNOSTIC SUMMARY ##
    ###############################

    # Pull plate groups
    CorScore = self.plate_groups

    # If the data is BinaryClass where plate and well information is available, do the following
    if hasattr(self, "value"):

        # First, only keep the values that aren't being filtered
        CorScore = CorScore.loc[CorScore["bmdrc.filter"] == "Keep", [self.concentration, "bmdrc.Endpoint.ID", "bmdrc.num.nonna", "bmdrc.num.affected"]]

        # Sum up counts
        CorScore = CorScore.groupby([self.concentration, "bmdrc.Endpoint.ID"]).sum().reset_index()

        # Calculate response
        CorScore["Response"] = CorScore["bmdrc.num.affected"] / CorScore["bmdrc.num.nonna"]

    else:

        # Calculate the response
        CorScore = CorScore.loc[CorScore["bmdrc.filter"] == "Keep", [self.concentration, "bmdrc.Endpoint.ID", self.response]].rename(columns = {self.response:"Response"})

    # Sort data.frame appropriately
    CorScore.sort_values(by = ["bmdrc.Endpoint.ID", self.concentration])

    # Calculate spearman correlations
    CorScore = CorScore[[self.concentration, "bmdrc.Endpoint.ID", "Response"]].groupby(["bmdrc.Endpoint.ID"]).corr(method = "spearman").unstack().iloc[:,1].reset_index()

    # Fix index issues 
    CorScore = CorScore.set_axis(["bmdrc.Endpoint.ID", "Spearman"], axis = 1)

    # Set NA values (cases of a consistent value across all wells) to 0
    CorScore.loc[np.isnan(CorScore["Spearman"]), "Spearman"] = 0

    # Set the filter to leep
    CorScore["Filter"] = "Keep"

    # Filter cases with less than 0.2 as their correlation score
    CorScore.loc[CorScore["Spearman"] < score, "Filter"] = "Remove"

    # Add correlation summary object to object
    self.filter_correlation_score_df = CorScore
    self.filter_correlation_score_thresh = score
    self.filter_correlation_score_plot = __correlation_score_plot(CorScore, score)

    #######################
    ## RETURN DIAGNOSTIC ##
    #######################
    
    if apply == False:
        if diagnostic_plot == False:
            plt.close(self.filter_correlation_score_plot)

    #############################
    ## OTHERWISE, APPLY FILTER ##
    #############################

    else:

        # Get list of removals 
        removal_list = CorScore.loc[CorScore["Filter"] == "Remove", "bmdrc.Endpoint.ID"].tolist()

        # Remove values
        self.plate_groups.loc[self.plate_groups["bmdrc.Endpoint.ID"].isin(removal_list), "bmdrc.filter"] = "Remove"
        self.plate_groups.loc[self.plate_groups["bmdrc.Endpoint.ID"].isin(removal_list), "bmdrc.filter.reason"] = \
            self.plate_groups.loc[self.plate_groups["bmdrc.Endpoint.ID"].isin(removal_list), "bmdrc.filter.reason"] + " correlation_score_filter"
