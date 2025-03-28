from graphviz import Digraph

def generate_wireframe():
    wireframe = Digraph("GenAI Web Application", format='png')
    wireframe.attr(rankdir='TB', size='10')
    
    # Pages
    wireframe.node("Home", shape="rect", style="filled", fillcolor="lightblue")
    wireframe.node("Signup/Signin", shape="rect", style="filled", fillcolor="lightgrey")
    wireframe.node("Ratings", shape="rect", style="filled", fillcolor="lightgrey")
    wireframe.node("Dashboard", shape="rect", style="filled", fillcolor="lightgreen")
    wireframe.node("ASKDOC AI", shape="rect", style="filled", fillcolor="lightyellow")
    
    # Dashboard Features
    wireframe.node("Tasks", shape="ellipse", style="filled", fillcolor="white")
    wireframe.node("Task Progress %", shape="ellipse", style="filled", fillcolor="white")
    wireframe.node("Daily Quote", shape="ellipse", style="filled", fillcolor="white")
    wireframe.node("Streak Count", shape="ellipse", style="filled", fillcolor="white")
    wireframe.node("Reminders", shape="ellipse", style="filled", fillcolor="white")
    wireframe.node("Alerts", shape="ellipse", style="filled", fillcolor="white")
    
    # Dropdown List
    wireframe.node("Settings", shape="parallelogram", style="filled", fillcolor="white")
    wireframe.node("View Profile", shape="parallelogram", style="filled", fillcolor="white")
    wireframe.node("Logout", shape="parallelogram", style="filled", fillcolor="white")
    
    # Home Page Sections
    wireframe.node("Features", shape="ellipse", style="filled", fillcolor="white")
    wireframe.node("Healthy Practices", shape="ellipse", style="filled", fillcolor="white")
    wireframe.node("Meet Our Team", shape="ellipse", style="filled", fillcolor="white")
    wireframe.node("Contact Us", shape="ellipse", style="filled", fillcolor="white")
    
    # Connections
    wireframe.edge("Home", "Signup/Signin")
    wireframe.edge("Home", "Ratings")
    wireframe.edge("Home", "Dashboard")
    wireframe.edge("Home", "ASKDOC AI")
    wireframe.edge("Dashboard", "Tasks")
    wireframe.edge("Dashboard", "Task Progress %")
    wireframe.edge("Dashboard", "Daily Quote")
    wireframe.edge("Dashboard", "Streak Count")
    wireframe.edge("Dashboard", "Reminders")
    wireframe.edge("Dashboard", "Alerts")
    wireframe.edge("Dashboard", "Settings")
    wireframe.edge("Dashboard", "View Profile")
    wireframe.edge("Dashboard", "Logout")
    wireframe.edge("Home", "Features")
    wireframe.edge("Home", "Healthy Practices")
    wireframe.edge("Home", "Meet Our Team")
    wireframe.edge("Home", "Contact Us")
    wireframe.edge("ASKDOC AI", "Chatbot")
    wireframe.edge("ASKDOC AI", "Upload Prescription")
    
    # Render the wireframe diagram
    wireframe.render("genai_wireframe", view=True)

# Generate the wireframe
generate_wireframe()
