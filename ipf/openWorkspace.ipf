// Create a new workspace with a dedicated virtual environment
// This will prompt you to select the project folder, and it will either
// create or activate the named python virtual environment, and install all dependencies
// specified in the requirements.txt file
function openWorkspace(String environmentName)

	NewPath/O/Q/Z workspace
	if (V_flag)
		return 0
	endif
	
	String folderNames = IndexedDir(workspace, -1, 0, ";")
	if (WhichListItem(environmentName, folderNames, ";") == -1)
		// environment doesn't exist yet, create it
		print "Creating virtual Python environment in workspace..."
		PythonEnv/P=workspace venv = environmentName
	endif
	
	// Activate the environment
	print "Activating " + environmentName + "..."
	PythonEnv/P=workspace activate = environmentName
	
	// Try to find a requirements.txt file, and install dependencies
	String fileNames = IndexedFile(workspace, -1, ".txt")
	if (WhichListItem("requirements.txt", fileNames) != -1)
		PathInfo workspace
		String requirementsPath = ParseFilePath(5, S_path + "requirements.txt", "\\", 0, 0)
		print "Installing requirements..."
		installPackage("-r " + requirementsPath)
	endif
	
	// Change the Python working directory to the workspace folder
	// Changing all the path separators to forward slash for safety
	String homeFolder = StringByKey("HOME",S_PythonEnvInfo, "=",";")
	homeFolder = ParseFilePath(1, homeFolder, "\\", 1, 0) 
	homeFolder = RemoveEnding(ReplaceString("\\", homeFolder, "/"),"/")
	
	Python execute = "import os"
	Python execute = "os.chdir('" + homeFolder + "')"	
end

// Install a Python package into the active environment
function installPackage(String arguments)
	// Get the path to the Python executable
	PythonEnv
	String pathToPip = StringByKey("HOME", S_PythonEnvInfo, "=", ";") + "\\Scripts\\pip.exe"
	
	// Build the pip install command string
	String cmd
	sprintf cmd, "\"%s\" install %s", pathToPip, arguments
	
	ExecuteScriptText/B/Z cmd
	print S_Value
end
