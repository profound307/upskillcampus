from flask import Flask, jsonify, request, render_template
from manager import StudentManager
import os

app = Flask(__name__)

# Initialize the manager. It will load/save data from data/students.json
manager = StudentManager()

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/students", methods=["GET"])
def get_students():
    sort_by = request.args.get("sort", None)
    reverse = request.args.get("reverse", "false").lower() == "true"
    
    if sort_by == "name":
        students = manager.get_sorted_by_name(reverse=reverse)
    elif sort_by == "marks":
        students = manager.get_sorted_by_marks(reverse=reverse)
    else:
        students = manager.view_students()
        
    return jsonify([s.to_dict() for s in students])

@app.route("/api/students/<student_id>", methods=["GET"])
def get_student(student_id):
    student = manager.search_student(student_id)
    if student:
        return jsonify(student.to_dict())
    return jsonify({"error": f"Student with ID '{student_id}' not found."}), 404

@app.route("/api/students", methods=["POST"])
def add_student():
    data = request.json or {}
    required_fields = ["student_id", "name", "age", "gender", "course", "marks", "email", "description"]
    for field in required_fields:
        if field not in data or data[field] == "":
            return jsonify({"error": f"Field '{field}' is required and cannot be empty."}), 400
            
    try:
        new_student = manager.add_student(
            student_id=data["student_id"],
            name=data["name"],
            age=data["age"],
            gender=data["gender"],
            course=data["course"],
            marks=data["marks"],
            email=data["email"],
            description=data["description"]
        )
        return jsonify(new_student.to_dict()), 201
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

@app.route("/api/students/<student_id>", methods=["PUT"])
def update_student(student_id):
    data = request.json or {}
    try:
        updated_student = manager.update_student(
            student_id=student_id,
            name=data.get("name"),
            age=data.get("age"),
            gender=data.get("gender"),
            course=data.get("course"),
            marks=data.get("marks"),
            email=data.get("email"),
            description=data.get("description")
        )
        return jsonify(updated_student.to_dict())
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

@app.route("/api/students/<student_id>", methods=["DELETE"])
def delete_student(student_id):
    try:
        manager.delete_student(student_id)
        return jsonify({"success": f"Student with ID '{student_id}' has been deleted."})
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

@app.route("/api/stats", methods=["GET"])
def get_stats():
    students = manager.view_students()
    total = len(students)
    
    grade_counts = {"A": 0, "B": 0, "C": 0, "D": 0, "E": 0, "F": 0}
    pass_fail_counts = {"Pass": 0, "Fail": 0}
    course_stats = {}
    
    if total == 0:
        avg_marks = 0.0
        course_counts = {}
    else:
        avg_marks = sum(s.marks for s in students) / total
        
        course_counts = {}
        for s in students:
            c = s.course
            course_counts[c] = course_counts.get(c, 0) + 1
            
            # Grade distribution
            g = s.grade
            if g in grade_counts:
                grade_counts[g] += 1
                
            # Pass/Fail distribution
            status = s.status
            if status in pass_fail_counts:
                pass_fail_counts[status] += 1
                
            # Course-wise details
            if c not in course_stats:
                course_stats[c] = {"marks_sum": 0.0, "student_count": 0, "pass_count": 0}
            course_stats[c]["marks_sum"] += s.marks
            course_stats[c]["student_count"] += 1
            if s.status == "Pass":
                course_stats[c]["pass_count"] += 1
                
        # Format course details
        course_details = []
        for course_name, cdata in course_stats.items():
            cnt = cdata["student_count"]
            avg = cdata["marks_sum"] / cnt if cnt > 0 else 0.0
            p_cnt = cdata["pass_count"]
            p_rate = (p_cnt / cnt) * 100 if cnt > 0 else 0.0
            course_details.append({
                "course_name": course_name,
                "student_count": cnt,
                "average_marks": round(avg, 2),
                "pass_count": p_cnt,
                "pass_rate": round(p_rate, 2)
            })
            
    return jsonify({
        "total_students": total,
        "average_marks": round(avg_marks, 2),
        "course_distribution": course_counts,
        "grade_distribution": grade_counts,
        "pass_fail_distribution": pass_fail_counts,
        "course_details": course_details if total > 0 else []
    })

if __name__ == "__main__":
    app.run(debug=True)
