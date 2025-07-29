import os
import sys
import json as _json
import dotenv
import webbrowser
import requests  # Add this import
import datetime  # Add this import
import pytz      # Add this import

# Load .env from the current working directory
dotenv.load_dotenv(dotenv_path=os.path.join(os.getcwd(), ".env"), override=True)

# Try loading from home directory if variables are still not set
if not os.environ.get("LANGFUSE_PUBLIC_KEY") or not os.environ.get("LANGFUSE_SECRET_KEY") or not os.environ.get("LANGFUSE_HOST"):
    dotenv.load_dotenv(dotenv_path=os.path.expanduser("~/.env"), override=True)

# Final check before exiting
missing_vars = []
if not os.environ.get("LANGFUSE_PUBLIC_KEY"):
    missing_vars.append("LANGFUSE_PUBLIC_KEY")
if not os.environ.get("LANGFUSE_SECRET_KEY"):
    missing_vars.append("LANGFUSE_SECRET_KEY")
if not os.environ.get("LANGFUSE_HOST"):
    missing_vars.append("LANGFUSE_HOST")

if missing_vars:
    print(f"Error: {', '.join(missing_vars)} not found.")
    sys.exit(1)

from langfuse import Langfuse
import os
import sys
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

_DEBUG_=False
if _DEBUG_:
    print(os.environ.get("LANGFUSE_PUBLIC_KEY"))
    print(os.environ.get("LANGFUSE_SECRET_KEY"))
    print(os.environ.get("LANGFUSE_HOST"))

langfuse = Langfuse(
    public_key=os.environ.get("LANGFUSE_PUBLIC_KEY"),
    secret_key=os.environ.get("LANGFUSE_SECRET_KEY"),
    host=os.environ.get("LANGFUSE_HOST"),
    release=os.environ.get("LANGFUSE_RELEASE", None)
)
    
def open_trace_in_browser(trace_id):
    base_url = os.environ.get("LANGFUSE_HOST")
    project_id = os.environ.get("LANGFUSE_PROJECT_ID")
    if not base_url or not project_id:
        print("Missing LANGFUSE_HOST or LANGFUSE_PROJECT_ID")
        return
    full_url = f"{base_url}/project/{project_id}/traces/{trace_id}"
    print(f"Opening {full_url}")
    webbrowser.open(full_url)

def get_score_by_id(score_id):
    """Retrieve score details by score ID."""
    base_url = os.environ.get("LANGFUSE_HOST")
    public_key = os.environ.get("LANGFUSE_PUBLIC_KEY")
    secret_key = os.environ.get("LANGFUSE_SECRET_KEY")
    url = f"{base_url}/api/public/scores/{score_id}"
    try:
        response = requests.get(url, auth=(public_key, secret_key))
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"Error retrieving score {score_id}: {e}")
        return None

def list_scores():
    """Retrieve all score configurations."""
    base_url = os.environ.get("LANGFUSE_HOST")
    public_key = os.environ.get("LANGFUSE_PUBLIC_KEY")
    secret_key = os.environ.get("LANGFUSE_SECRET_KEY")
    url = f"{base_url}/api/public/scores"
    try:
        response = requests.get(url, auth=(public_key, secret_key))
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"Error retrieving scores: {e}")
        return None

def print_trace(trace, show_comments=False):
    print(f"<Trace \n\tat=\"{trace.createdAt}\" \n\tid=\"{trace.id}\" \n\tname=\"{trace.name}\" \n\tsession_id=\"{trace.session_id}\" \n\tprojectId=\"{trace.projectId}\" >")
    print(f"<Input><CDATA[[\n{trace.input}\n]]></Input>")
    print(f"<Output><CDATA[[\n{trace.output}\n]]></Output>")
    if trace.metadata:
        print(f"<Metadata>{trace.metadata}</Metadata>")
    if trace.scores:
        print("<Scores>")
        for score_id in trace.scores:
            score = get_score_by_id(score_id)
            if score:
                print(f"<Score name=\"{score['name']}\" value=\"{score['value']}\" data_type=\"{score['dataType']}\" />")
        print("</Scores>")
    if show_comments and hasattr(trace, "comments"):
        print(f"<Comments>\n{trace.comments}\n</Comments>")
    print("</Trace>")

def print_traces(traces, show_comments=False):
    for trace in traces.data:
        print_trace(trace, show_comments)

def list_traces(limit=100, output_dir="../output/traces", show_comments=False):
    traces = langfuse.get_traces(limit=limit)
    os.makedirs(output_dir, exist_ok=True)
    return traces

def list_traces_by_score(score_name, min_value=None, max_value=None, limit=100):
    traces = langfuse.get_traces(limit=limit)
    filtered_traces = []
    for trace in traces.data:
        for score_id in trace.scores:
            score = get_score_by_id(score_id)
            if score and score.get('name') == score_name:
                if (min_value is None or score.get('value') >= min_value) and (max_value is None or score.get('value') <= max_value):
                    filtered_traces.append(trace)
                    break
    return filtered_traces

def add_score_to_a_trace(trace_id, generation_id, name, value, data_type="NUMERIC", comment=""):
    result_add_score_to_a_trace=langfuse.score(
        trace_id=trace_id,
        observation_id=generation_id,
        name=name,
        value=value,
        data_type=data_type,
        comment=comment
    )
    return result_add_score_to_a_trace

def create_score(name, data_type, description="", possible_values=None, min_value=None, max_value=None):
    placeholder_value = ""
    if data_type.upper() == "BOOLEAN":
        placeholder_value = "1"

    resulting_score = langfuse.score(
        name=name,
        value=placeholder_value,
        data_type=data_type,
        description=description,
        # For categorical:
        **({"possible_values": possible_values} if data_type == "CATEGORICAL" and possible_values else {}),
        # For numeric:
        **({"min_value": min_value, "max_value": max_value} if data_type == "NUMERIC" and min_value is not None and max_value is not None else {})
    )
    return resulting_score

def score_exists(name):
    """
    Check if a score with the given name exists by calling list_scores().
    """
    scores = list_scores()
    if not scores or scores.get('meta', {}).get('totalItems', 0) == 0:
        return False
    for sc in scores:
        if sc.get("name") == name:
            return True
    return False

def create_dataset(name, description="", metadata=None):
    langfuse.create_dataset(
        name=name,
        description=description,
        metadata=metadata or {}
    )
def get_dataset(name) :
    return langfuse.get_dataset(name=name)
  
def create_prompt(name, prompt_text, model_name, temperature, labels=None, supported_languages=None):
    langfuse.create_prompt(
        name=name,
        type="text", 
        prompt=prompt_text,
        labels=labels or [],
        config={
            "model": model_name,
            "temperature": temperature,
            "supported_languages": supported_languages or [],
        }
    )
def get_prompt(name, label="production"):
    return langfuse.get_prompt(name=name,label=label)
  
def update_prompt(name, new_prompt_text):
    prompt = langfuse.get_prompt(name=name)
    prompt.update(prompt=new_prompt_text)

def delete_dataset(name):
    dataset = langfuse.get_dataset(name=name)
    dataset.delete()

def get_trace_by_id(trace_id):
    return langfuse.get_trace(trace_id)

def search_traces(
    start_date=None,
    end_date=None,
    keywords=None,
    tags=None,
    metadata_filters=None,
    limit=100
):
    """
    Search and filter traces based on date range, keywords, tags, and metadata.

    Parameters:
        start_date (str): ISO format date string for the start of the date range.
        end_date (str): ISO format date string for the end of the date range.
        keywords (list): List of keywords to search in input or output.
        tags (list): List of tags to filter traces.
        metadata_filters (dict): Dictionary of metadata key-value pairs for filtering.
        limit (int): Number of traces to fetch.

    Returns:
        list: Filtered list of traces.
    """
    try:
        params = {}
        if start_date:
            from_timestamp = datetime.datetime.fromisoformat(start_date)
            from_timestamp = from_timestamp.replace(tzinfo=pytz.UTC)
            params['from_timestamp'] = from_timestamp
        if end_date:
            to_timestamp = datetime.datetime.fromisoformat(end_date)
            to_timestamp = to_timestamp.replace(tzinfo=pytz.UTC)
            params['to_timestamp'] = to_timestamp
        if tags:
            params['tags'] = tags
        if metadata_filters:
            for key, value in metadata_filters.items():
                params[f'metadata.{key}'] = value

        traces = langfuse.get_traces(limit=limit, **params)
        if not traces:
            return []

        filtered_traces = traces.data

        if keywords:
            keyword_set = set(keyword.lower() for keyword in keywords)
            filtered_traces = [
                trace for trace in filtered_traces
                if any(keyword in trace.input.lower() for keyword in keyword_set) or
                   any(keyword in trace.output.lower() for keyword in keyword_set)
            ]

        return filtered_traces
    except Exception as e:
        print(f"Error searching traces: {e}")
        return []

def fetch_all_traces(start_date=None, end_date=None):
    all_traces = []
    page = 1
    chunk_size = 100
    params = {}
    if start_date:
        params['from_timestamp'] = datetime.datetime.fromisoformat(start_date).replace(tzinfo=pytz.UTC)
    if end_date:
        params['to_timestamp'] = datetime.datetime.fromisoformat(end_date).replace(tzinfo=pytz.UTC)
    
    while True:
        partial = langfuse.get_traces(limit=chunk_size, page=page, **params)
        if not partial or not partial.data:
            break
        all_traces.extend(partial.data)
        if len(partial.data) < chunk_size:
            break
        page += 1
    return all_traces

def export_traces(format='json', output_path=None, start_date=None, end_date=None):
    """
    Export traces along with their full score details.
    """
    try:
        all_traces = fetch_all_traces(start_date=start_date, end_date=end_date)
        if not output_path:
            output_path = f"./traces_export.{format}"

        # Ensure the output directory exists
        output_dir = os.path.dirname(output_path)
        if output_dir and not os.path.exists(output_dir):
            os.makedirs(output_dir)

        all_scores=list_scores()
        exported_data = []
        for t in all_traces:
            # fetch full score details
            score_details = []
            if t.scores:
                for s_id in t.scores:
                    s_detail = get_score_by_id(s_id)
                    if s_detail:
                        score_details.append(s_detail)
            t_dict = t.__dict__
            t_dict["score_details"] = score_details
            exported_data.append(t_dict)

        if format == 'json':
            with open(output_path, 'w') as f:
                _json.dump(exported_data, f, indent=2, default=str)
        elif format == 'csv':
            import csv
            fieldnames = ['id', 'name', 'input', 'output', 'createdAt']
            with open(output_path, 'w', newline='') as f:
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                writer.writeheader()
                for t in all_traces:
                    writer.writerow({
                        'id': t.id,
                        'name': t.name,
                        'input': t.input,
                        'output': t.output,
                        'createdAt': str(t.createdAt)
                    })

        if all_traces:
            # Sort traces by createdAt to ensure the oldest date is first
            all_traces.sort(key=lambda x: x.createdAt)
            first_trace_date = datetime.datetime.fromisoformat(all_traces[0].createdAt.replace('Z', '+00:00')).strftime('%Y-%m-%d %H:%M:%S')
            last_trace_date = datetime.datetime.fromisoformat(all_traces[-1].CreatedAt.replace('Z', '+00:00')).strftime('%Y-%m-%d %H:%M:%S')
            print(f"Traces exported to {output_path}. Total traces exported: {len(all_traces)}")
            print(f"Date range: {first_trace_date} to {last_trace_date}")
        else:
            print(f"Traces exported to {output_path}. Total traces exported: {len(all_traces)}")
    except Exception as e:
        print(f"Error exporting traces: {e}")

def create_new_trace(name, input_text, output_text, session_id=None, metadata=None, timestamp=None):
    """
    Creates a new trace with an optional timestamp.
    """
    parsed_timestamp = None
    if timestamp:
        try:
            parsed_timestamp = datetime.datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
        except ValueError:
            pass
    trace_created=langfuse.trace(
        name=name,
        input=input_text,
        output=output_text,
        session_id=session_id,
        metadata=metadata,
        timestamp=parsed_timestamp
    )
    return trace_created

def import_traces(format='json', input_path=None):
    """
    Import traces. If any score doesn't exist, create it and attach it to the trace.
    """
    if not input_path:
        print("No input file provided for importing traces.")
        return

    try:
        if format == 'json':
            with open(input_path, 'r') as f:
                data = _json.load(f)
        elif format == 'csv':
            import csv
            data = []
            with open(input_path, 'r', newline='') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    data.append(row)

        if isinstance(data, dict):
            data = [data]

        # Create new traces in Langfuse from data
        for item in data:
            trace_timestamp = item.get('timestamp') or item.get('createdAt')
            new_trace = create_new_trace(
                name=item.get('name', 'Imported Trace'),
                input_text=item.get('input', ''),
                output_text=item.get('output', ''),
                session_id=item.get('session_id'),
                metadata=item.get('metadata'),
                timestamp=trace_timestamp
            )
            # handle imported scores
            for s_detail in item.get("score_details", []):
                score_name = s_detail["name"]
                score_value = str(s_detail.get("value", "0"))
                score_data_type = s_detail.get("dataType", "NUMERIC")
                score_comment = s_detail.get("comment", "")
                score_description = s_detail.get("description", "")
                score_possible_values = s_detail.get("possible_values")
                minimum_score_value = s_detail.get("min_value")
                max_score_value = s_detail.get("max_value")
                if not score_exists(score_name):
                    resulting_score=create_score(
                        name=score_name,
                        data_type=score_data_type,
                        description=score_description,
                        possible_values=score_possible_values,
                        min_value=minimum_score_value,
                        max_value=max_score_value
                        
                    )
                result_add_score_to_a_trace=add_score_to_a_trace(
                    trace_id=new_trace.id,
                    generation_id=None,  # Replace as needed if your data includes observation IDs
                    name=score_name,
                    value=score_value,
                    data_type=score_data_type,
                    comment=score_comment
                )
                print(f"Added score {score_name} to trace {new_trace.id}")
                print(result_add_score_to_a_trace)
                
        print(f"Imported {len(data)} traces from {input_path}")
    except Exception as e:
        print(f"Error importing traces: {e}")

def list_sessions(limit=100, start_date=None, end_date=None):
    """
    List all sessions with optional date filtering.
    Retrieves multiple pages so we don't miss older sessions.
    """
    base_url = os.environ.get("LANGFUSE_HOST")
    public_key = os.environ.get("LANGFUSE_PUBLIC_KEY")
    secret_key = os.environ.get("LANGFUSE_SECRET_KEY")
    url = f"{base_url}/api/public/sessions"
    sessions = []
    page = 1
    while True:
        params = {
            "page": page,
            "limit": limit
        }
        if start_date:
            params["fromTimestamp"] = datetime.datetime.fromisoformat(start_date).isoformat() + 'Z'
        if end_date:
            params["toTimestamp"] = datetime.datetime.fromisoformat(end_date).isoformat() + 'Z'
        
        try:
            response = requests.get(url, auth=(public_key, secret_key), params=params)
            response.raise_for_status()
            data = response.json()
        except Exception as e:
            print(f"Error retrieving sessions: {e}")
            break
        
        if "data" not in data or len(data["data"]) == 0:
            break
        
        sessions.extend(data["data"])
        if len(data["data"]) < limit:
            break
        page += 1
    
    return sessions

def get_session(session_id):
    """
    Get details of a specific session including its traces.
    """
    base_url = os.environ.get("LANGFUSE_HOST")
    public_key = os.environ.get("LANGFUSE_PUBLIC_KEY")
    secret_key = os.environ.get("LANGFUSE_SECRET_KEY")
    url = f"{base_url}/api/public/sessions/{session_id}"

    try:
        response = requests.get(url, auth=(public_key, secret_key))
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"Error retrieving session {session_id}: {e}")
        return None

def get_upload_url(trace_id, content_type, content_length):
    """
    Get a presigned URL for media upload.
    """
    # TODO: Implement API call to POST /media
    pass

def get_media(media_id):
    """
    Retrieve media record details.
    """
    # TODO: Implement API call to GET /media/{mediaId}
    pass

def get_daily_metrics(trace_name=None, user_id=None, tags=None, from_timestamp=None, to_timestamp=None):
    """
    Get daily metrics with optional filtering.
    """
    # TODO: Implement API call to GET /metrics/daily with query params
    pass

def list_prompts(name=None, label=None, tag=None, limit=100, start_date=None, end_date=None):
    """
    List prompts with optional filtering.
    """
    base_url = os.environ.get("LANGFUSE_HOST")
    public_key = os.environ.get("LANGFUSE_PUBLIC_KEY")
    secret_key = os.environ.get("LANGFUSE_SECRET_KEY")
    url = f"{base_url}/api/public/v2/prompts"
    params = {"limit": limit}
    if name:
        params["name"] = name
    if label:
        params["label"] = label
    if tag:
        params["tag"] = tag
    if start_date:
        params["fromUpdatedAt"] = datetime.datetime.fromisoformat(start_date).isoformat() + 'Z'
    if end_date:
        params["toUpdatedAt"] = datetime.datetime.fromisoformat(end_date).isoformat() + 'Z'
    try:
        response = requests.get(url, auth=(public_key, secret_key), params=params)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"Error retrieving prompts: {e}")
        return None