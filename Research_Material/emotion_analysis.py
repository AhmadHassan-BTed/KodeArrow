# import pandas as pd
# import seaborn as sns
# import matplotlib.pyplot as plt
# from sklearn.linear_model import LinearRegression
# import numpy as np

# # Provided data
# data = {
#     "Valence": ["Negative", "Negative", "Negative", "Neutral", "Neutral", "Neutral", "Positive", "Positive", "Positive"],
#     "Arousal": ["Low", "Medium", "High", "Low", "Medium", "High", "Low", "Medium", "High"],
#     "Keystroke Duration": [0.1049, 0.0922, 0.0946, 0.0944, 0.0933, 0.0942, 0.0953, 0.0950, 0.0931],
#     "Keystroke Latency": [0.1182, 0.1472, 0.1444, 0.1424, 0.1544, 0.1295, 0.1347, 0.1404, 0.1316],
#     "Accuracy Rate": [0.914, 0.784, 0.907, 0.942, 0.879, 0.820, 0.862, 0.869, 0.855]
# }

# df = pd.DataFrame(data)

# # Encoding categorical variables (Valence and Arousal)
# df['Valence_encoded'] = df['Valence'].map({'Negative': 0, 'Neutral': 1, 'Positive': 2})
# df['Arousal_encoded'] = df['Arousal'].map({'Low': 0, 'Medium': 1, 'High': 2})

# # Prepare data for regression
# X = df[['Valence_encoded', 'Arousal_encoded']]
# y_duration = df['Keystroke Duration']
# y_latency = df['Keystroke Latency']
# y_accuracy = df['Accuracy Rate']

# # Fit regression models
# reg_duration = LinearRegression().fit(X, y_duration)
# reg_latency = LinearRegression().fit(X, y_latency)
# reg_accuracy = LinearRegression().fit(X, y_accuracy)

# # Predict values
# df['Predicted_Duration'] = reg_duration.predict(X)
# df['Predicted_Latency'] = reg_latency.predict(X)
# df['Predicted_Accuracy'] = reg_accuracy.predict(X)

# # Plot Regression Plots
# plt.figure(figsize=(15, 5))

# # Keystroke Duration vs Valence and Arousal
# plt.subplot(1, 3, 1)
# sns.scatterplot(x=df['Valence_encoded'], y=df['Keystroke Duration'], hue=df['Arousal'], palette='coolwarm')
# sns.lineplot(x=df['Valence_encoded'], y=df['Predicted_Duration'], color='black', label='Regression Line')
# plt.title('Keystroke Duration vs Emotion')
# plt.xlabel('Valence (Encoded)')
# plt.ylabel('Keystroke Duration (seconds)')

# # Keystroke Latency vs Valence and Arousal
# plt.subplot(1, 3, 2)
# sns.scatterplot(x=df['Valence_encoded'], y=df['Keystroke Latency'], hue=df['Arousal'], palette='coolwarm')
# sns.lineplot(x=df['Valence_encoded'], y=df['Predicted_Latency'], color='black', label='Regression Line')
# plt.title('Keystroke Latency vs Emotion')
# plt.xlabel('Valence (Encoded)')
# plt.ylabel('Keystroke Latency (seconds)')

# # Accuracy Rate vs Valence and Arousal
# plt.subplot(1, 3, 3)
# sns.scatterplot(x=df['Valence_encoded'], y=df['Accuracy Rate'], hue=df['Arousal'], palette='coolwarm')
# sns.lineplot(x=df['Valence_encoded'], y=df['Predicted_Accuracy'], color='black', label='Regression Line')
# plt.title('Accuracy Rate vs Emotion')
# plt.xlabel('Valence (Encoded)')
# plt.ylabel('Accuracy Rate')

# plt.tight_layout()
# # plt.show()

###########################################3
# import pandas as pd
# import numpy as np
# import matplotlib.pyplot as plt
# from mpl_toolkits.mplot3d import Axes3D

# # Data
# data = {
#     "Valence": ["Negative", "Negative", "Negative", "Neutral", "Neutral", "Neutral", "Positive", "Positive", "Positive"],
#     "Arousal": ["Low", "Medium", "High", "Low", "Medium", "High", "Low", "Medium", "High"],
#     "Keystroke Duration": [0.1049, 0.0922, 0.0946, 0.0944, 0.0933, 0.0942, 0.0953, 0.0950, 0.0931],
#     "Keystroke Latency": [0.1182, 0.1472, 0.1444, 0.1424, 0.1544, 0.1295, 0.1347, 0.1404, 0.1316],
#     "Accuracy Rate": [0.914, 0.784, 0.907, 0.942, 0.879, 0.820, 0.862, 0.869, 0.855]
# }

# df = pd.DataFrame(data)

# # Convert categorical Valence and Arousal to numerical for 3D plotting
# df["Valence_Num"] = df["Valence"].map({"Negative": -1, "Neutral": 0, "Positive": 1})
# df["Arousal_Num"] = df["Arousal"].map({"Low": 1, "Medium": 2, "High": 3})

# # Define a function to create 3D Bubble Plots
# def plot_3d_bubble(x, y, z, bubble_size, title, z_label):
#     fig = plt.figure(figsize=(10, 7))
#     ax = fig.add_subplot(111, projection='3d')
    
#     # Plot bubbles
#     scatter = ax.scatter(x, y, z, s=np.array(bubble_size) * 800, c=z, cmap="coolwarm", alpha=0.6, edgecolors="k")

#     # Labels
#     ax.set_xlabel("Valence (-1: Negative, 0: Neutral, 1: Positive)")
#     ax.set_ylabel("Arousal (1: Low, 2: Medium, 3: High)")
#     ax.set_zlabel(z_label)
#     ax.set_title(title)

#     # Color bar
#     cbar = plt.colorbar(scatter, shrink=0.6, aspect=10)
#     cbar.set_label(z_label)

#     plt.show()

# # 3D Bubble Plots for each metric
# plot_3d_bubble(df["Valence_Num"], df["Arousal_Num"], df["Keystroke Duration"], df["Keystroke Duration"], 
#                "3D Bubble Chart of Keystroke Duration", "Keystroke Duration (s)")

# plot_3d_bubble(df["Valence_Num"], df["Arousal_Num"], df["Keystroke Latency"], df["Keystroke Latency"], 
#                "3D Bubble Chart of Keystroke Latency", "Keystroke Latency (s)")

# plot_3d_bubble(df["Valence_Num"], df["Arousal_Num"], df["Accuracy Rate"], df["Accuracy Rate"], 
#                "3D Bubble Chart of Accuracy Rate", "Accuracy Rate")

################################

# import pandas as pd
# import numpy as np
# import matplotlib.pyplot as plt
# from mpl_toolkits.mplot3d import Axes3D
# from sklearn.preprocessing import LabelEncoder
# from sklearn.linear_model import LinearRegression

# # Provided data
# data = {
#     "Valence": ["Negative", "Negative", "Negative", "Neutral", "Neutral", "Neutral", "Positive", "Positive", "Positive"],
#     "Arousal": ["Low", "Medium", "High", "Low", "Medium", "High", "Low", "Medium", "High"],
#     "Keystroke Duration": [0.1049, 0.0922, 0.0946, 0.0944, 0.0933, 0.0942, 0.0953, 0.0950, 0.0931],
#     "Keystroke Latency": [0.1182, 0.1472, 0.1444, 0.1424, 0.1544, 0.1295, 0.1347, 0.1404, 0.1316],
#     "Accuracy Rate": [0.914, 0.784, 0.907, 0.942, 0.879, 0.820, 0.862, 0.869, 0.855]
# }

# df = pd.DataFrame(data)

# # Encoding Valence and Arousal to numeric values
# valence_encoder = LabelEncoder()
# arousal_encoder = LabelEncoder()
# df["Valence_Num"] = valence_encoder.fit_transform(df["Valence"])  # Negative=0, Neutral=1, Positive=2
# df["Arousal_Num"] = arousal_encoder.fit_transform(df["Arousal"])  # Low=0, Medium=1, High=2

# # 3D Plot: Valence, Arousal, Keystroke Duration
# fig = plt.figure(figsize=(10, 6))
# ax = fig.add_subplot(111, projection='3d')

# x = df["Valence_Num"]
# y = df["Arousal_Num"]
# z = df["Keystroke Duration"]

# # Scatter plot
# ax.scatter(x, y, z, c=z, cmap='coolwarm', label="Keystroke Duration")

# # Fitting a plane using regression
# X = np.column_stack((x, y))
# reg = LinearRegression().fit(X, z)
# xx, yy = np.meshgrid(np.linspace(0, 2, 10), np.linspace(0, 2, 10))
# zz = reg.predict(np.column_stack((xx.ravel(), yy.ravel()))).reshape(xx.shape)
# ax.plot_surface(xx, yy, zz, alpha=0.5, cmap='coolwarm')

# # Labels
# ax.set_xlabel('Valence (0=Negative, 1=Neutral, 2=Positive)')
# ax.set_ylabel('Arousal (0=Low, 1=Medium, 2=High)')
# ax.set_zlabel('Keystroke Duration')
# ax.set_title('3D Visualization of Keystroke Duration by Emotion')

# plt.show()

###############33
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
import statsmodels.api as sm
import plotly.graph_objects as go
from mpl_toolkits.mplot3d import Axes3D

# Provided data
data = {
    "Valence": ["Negative", "Negative", "Negative", "Neutral", "Neutral", "Neutral", "Positive", "Positive", "Positive"],
    "Arousal": ["Low", "Medium", "High", "Low", "Medium", "High", "Low", "Medium", "High"],
    "Keystroke Duration": [0.1049, 0.0922, 0.0946, 0.0944, 0.0933, 0.0942, 0.0953, 0.0950, 0.0931],
    "Keystroke Latency": [0.1182, 0.1472, 0.1444, 0.1424, 0.1544, 0.1295, 0.1347, 0.1404, 0.1316],
    "Accuracy Rate": [0.914, 0.784, 0.907, 0.942, 0.879, 0.820, 0.862, 0.869, 0.855]
}

df = pd.DataFrame(data)

# Map categorical values to numerical values
df["Valence"] = df["Valence"].map({"Negative": -1, "Neutral": 0, "Positive": 1})
df["Arousal"] = df["Arousal"].map({"Low": 1, "Medium": 2, "High": 3})

# Function to generate 3D Regression Surface (Matplotlib)
def plot_3d_regression(df, target_variable):
    fig = plt.figure(figsize=(8, 6))
    ax = fig.add_subplot(111, projection='3d')

    # Define predictors and target variable
    X = df[["Valence", "Arousal"]]
    X = sm.add_constant(X)  # Add constant for intercept
    y = df[target_variable]

    # Fit multiple linear regression model
    model = sm.OLS(y, X).fit()

    # Generate a meshgrid for surface plot
    valence_range = np.linspace(df["Valence"].min(), df["Valence"].max(), 30)
    arousal_range = np.linspace(df["Arousal"].min(), df["Arousal"].max(), 30)
    V, A = np.meshgrid(valence_range, arousal_range)
    
    # Predict target variable for grid points
    Z = model.params[0] + model.params[1] * V + model.params[2] * A

    # Scatter plot of actual data points
    ax.scatter(df["Valence"], df["Arousal"], y, c='r', marker='o', label="Actual Data")

    # Plot regression surface
    ax.plot_surface(V, A, Z, cmap="coolwarm", alpha=0.5)

    # Labels
    ax.set_xlabel("Valence (-1: Negative, 0: Neutral, 1: Positive)")
    ax.set_ylabel("Arousal (1: Low, 2: Medium, 3: High)")
    ax.set_zlabel(target_variable)
    ax.set_title(f"3D Regression Surface Plot of {target_variable} under independent variables valence x arousal")

    plt.legend()

    # Save the plot as a high-resolution image (300 DPI)
    plt.savefig(f"{target_variable}_3D_plot.png", dpi=300)
    plt.show()

# Generate and save HD plots for all three metrics
for metric in ["Keystroke Duration", "Keystroke Latency", "Accuracy Rate"]:
    plot_3d_regression(df, metric)

# Function for Interactive 3D Visualization (Plotly)
def interactive_3d_plot(df, target_variable):
    # Define predictors and target variable
    X = df[["Valence", "Arousal"]]
    X = sm.add_constant(X)  # Add constant for intercept
    y = df[target_variable]

    # Fit multiple linear regression model
    model = sm.OLS(y, X).fit()

    # Generate a meshgrid for surface plot
    valence_range = np.linspace(df["Valence"].min(), df["Valence"].max(), 30)
    arousal_range = np.linspace(df["Arousal"].min(), df["Arousal"].max(), 30)
    V, A = np.meshgrid(valence_range, arousal_range)
    
    # Predict target variable for grid points
    Z = model.params[0] + model.params[1] * V + model.params[2] * A

    # Create interactive 3D plot
    fig = go.Figure()

    # Add regression surface
    fig.add_trace(go.Surface(z=Z, x=V, y=A, colorscale="Viridis", opacity=0.7))

    # Add scatter plot of actual data points
    fig.add_trace(go.Scatter3d(
        x=df["Valence"], y=df["Arousal"], z=df[target_variable],
        mode="markers",
        marker=dict(size=5, color="red", opacity=1),
        name="Actual Data"
    ))

    # Layout settings
    fig.update_layout(
        title=f"Interactive 3D Regression: {target_variable}",
        scene=dict(
            xaxis_title="Valence (-1: Negative, 0: Neutral, 1: Positive)",
            yaxis_title="Arousal (1: Low, 2: Medium, 3: High)",
            zaxis_title=target_variable
        )
    )

    fig.show()

# Generate both Matplotlib & Plotly 3D plots for all three metrics
for metric in ["Keystroke Duration", "Keystroke Latency", "Accuracy Rate"]:
    plot_3d_regression(df, metric)  # Matplotlib static 3D plot
    interactive_3d_plot(df, metric)  # Plotly interactive 3D plot
