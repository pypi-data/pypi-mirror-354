import feedback_memory


def test_record_and_load_feedback(tmp_path):
    file = tmp_path / "fb.json"
    feedback_memory.record_feedback(True, path=str(file))
    feedback_memory.record_feedback(False, path=str(file))
    data = feedback_memory.load_feedback(path=str(file))
    assert data["success"] == 1
    assert data["failure"] == 1


def test_get_mood(tmp_path):
    file = tmp_path / "fb.json"
    feedback_memory.record_feedback(True, path=str(file))
    assert feedback_memory.get_mood(path=str(file)) == "happy"
    feedback_memory.record_feedback(False, path=str(file))
    feedback_memory.record_feedback(False, path=str(file))
    assert feedback_memory.get_mood(path=str(file)) == "sad"

