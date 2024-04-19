	1	DESCRIPTION
	•	The original dataset was downloaded as the “Variant III.csv” dataset from Kaggle: https://www.kaggle.com/datasets/sgpjesus/bank-account-fraud-dataset-neurips-2022
	•	Data Handling and Scientific Computing: Pandas for data manipulation, and NumPy for numerical computing.
	•	Statistical Tools: Boxcox from SciPy for data transformation.
	◦	Machine Learning Models and Preprocessing:
	▪	From Scikit-learn:
	▪	DummyClassifier, LogisticRegression, AdaBoostClassifier, RandomForestClassifier, KNeighborsClassifier, SVC, GaussianNB for classification tasks.
	▪	RFE for feature selection.
	▪	StandardScaler, MinMaxScaler for feature scaling.
	▪	PolynomialFeatures for feature engineering.
	▪	GridSearchCV for hyperparameter tuning.
	▪	From imbalanced-learn (imblearn):
	▪	SMOTE for oversampling imbalanced datasets.
	◦	Model Training and Evaluation Tools:
	◦	Various metrics like accuracy_score, precision_score, recall_score, f1_score, confusion_matrix, roc_curve, roc_auc_score, auc for evaluating model performance.
	◦	Data Visualization Libraries:
	◦	Matplotlib for basic plotting.
	◦	Seaborn for statistical data visualization.
	◦	Plotly for interactive and web-based visualization.
	◦	Jupyter Widgets for Interactive Plots:
	◦	ipywidgets for adding interactivity to plots.
	◦	Clustering and Dimensionality Reduction:
	◦	KMeans, PCA, GaussianMixture for clustering and dimensionality reduction tasks.
	◦	Additional Tools:
	◦	tqdm for progress bars to track long-running processes.

	2	INSTALLATION
	•	Download and Extract the Zip File Download the zip file from the repository and extract it to the local machine.
	•	Install Python Requirements All Python dependencies and requirements are listed at the top of each python file. To install them, run the following command: pip3 install -r requirements.txt

	3	EXECUTION
	•	Import CSV data at loading data in Data Cleaning script to select variables.
	•	Using selected variables to run Base Model, Method 1-Transformation, Method   2-Polynomial, Method 3-Clustering and Confusion Matrix
	•	As the code progresses, it will display intermediate outputs.
