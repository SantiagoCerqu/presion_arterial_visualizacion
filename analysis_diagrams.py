import plotly.express as px
import plotly.graph_objects as go




# * Normal line chat for every data

def plot_line_data(data, x_name, y_name, name):
    fig = px.line(
        data,
        x=x_name,
        y=y_name,
        markers=True,
        # text=y_name,
        title=f"{name.title()} en el año 2024"
    )
    return fig


# * HERE ARE THE FUNCTIONS FOR THE DIAGNOSIS OF SYSTOLIC, DIASTOLIC AND THE GENERAL

# Color rating
color_1 = "#8AC926" # Normal
color_2 = "#FFCA3A" # Elevated
color_3 = "#FF924C" # Hypertension Stage 1
color_4 = "#FF7655"  # Hypertension Stage 2
color_5 = "#FF595E" # Hypertensive Crisis


def systolic_pressure_color(systolic):
    """Determine the rate color range for the Gauge chart

    Parameters
    ----------
    systolic : int
        Systolic pressure.

    Returns
    -------
    str
        Returns the hexadecimal colour
    """
    if systolic < 140:
        return color_1
    
    elif 140 <= systolic < 150:
        return color_2
    
    elif 150 <= systolic < 160:
        return color_3
    
    elif 160 <= systolic < 180:
        return color_4
    
    elif systolic >= 180:
        return color_5

def diastolic_pressure_color(diastolic):
    """Determine the rate color range for the Gauge chart 

    Parameters
    ----------
    diastolic : int
        Diastolic pressure.

    Returns
    -------
    str
        Returns the hexadecimal colour
    """
    if diastolic < 90:
        return color_1
    
    elif 90 <= diastolic < 100:
        return color_3
    
    elif 100 <= diastolic < 120:
        return color_4
    
    elif diastolic >= 120:
        return color_5

def heart_rate(rate):
    """Determine the color range of the heart_rate

    Parameters
    ----------
    rate : int
        Heart rate.

    Returns
    -------
    tuple[str, str]
        Returns the hexadecimal colour of the rate and the level
    """
    if rate < 60:
        return [color_2, "Bradycardia"]
    
    elif 60 <= rate < 100:
        return [color_1, "Normal Resting Heart Rate"]
    
    elif 100 <= rate < 110:
        return [color_2, "Elevated Resting Heart Rate"]
    
    elif 110 <= rate < 130:
        return [color_4, "Mild Tachycardia"]
    
    elif 130 <= rate < 150:
        return [color_5, "Moderate Tachycardia"]


def saturation_color(saturation):
    """Determine the color range for the saturation

    Parameters
    ----------
    saturation : int
        Blood oxygen saturation level.

    Returns
    -------
    tuple[str, str]
        Returns the hexadecimal colour of the saturation and the level
    """

    if 95 <= saturation <= 100:
        return [color_1, "Normal"]
    
    elif 90 <= saturation < 95:
        return [color_2, "Mild Hypoxemia"]
    
    elif 85 <= saturation < 90:
        return [color_3, "Moderate Hypoxemia"]
    
    elif 80 <= saturation < 85:
        return [color_4, "Severe Hypoxemia"]
    
    elif saturation < 80:
        return [color_5, "Critical Hypoxemia"]

def general_pressure_color(systolic, diastolic):
    """Determine the rate color range for the Gauge chart

    Parameters
    ----------
    systolic : int
        The systolic pressure.
    diastolic : int
        The diastolic pressure.

    Returns
    -------
    tuple : [str, str]
        Returns the hexadecimal colour and the diagnostic.
    """

    if (systolic < 140) and (diastolic < 90):
        return [color_1, "normal"]
    
    elif (140 <= systolic < 150) and (diastolic < 90) :
        return [color_2, "elevated"]
    
    elif (150 <= systolic < 160) or (90 <= diastolic < 100):
        return [color_3, "hypertension stage 1"]
    
    elif (160 <= systolic < 180) or (100 <= diastolic < 120):
        return [color_4, "hypertension stage 2"]
    
    elif (systolic >= 180) or (diastolic >= 120):
        return [color_5, "hipertensive crisis"]



# * Gauge diagrams 

def plot_gauge(indicator_number,
               indicator_color,
               indicator_suffix,
               indicator_title,
               max_bound=200):
    
    fig = go.Figure(go.Indicator(
        value = indicator_number,
        mode = "gauge+number",
        domain = {"x":[0,1], "y": [0,1]},
        number = {
            "suffix": indicator_suffix,
            "font.size": 26
        },
        gauge = {
            "axis": {"range": [0, max_bound], "tickwidth":1},
            "bar": {"color": indicator_color}
        },
        title = {
            "text":indicator_title,
            "font": {"size": 28}
        }
        )
    )
    return fig
        


