from assistant.actions.files.open_file import OpenFileTool

tool = OpenFileTool()

result = tool.execute(
    path=r"C:\Users\acer\Downloads\Jagan_S_HR_Intern_Resume.pdf"
)

print(result)