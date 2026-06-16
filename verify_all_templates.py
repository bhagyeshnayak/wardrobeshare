import os
import glob
import re

# Identify templates directory
TEMPLATE_DIR = r'c:\Users\NAYAK BHAGYESH\Desktop\wardrobeshare\templates'

def scan_templates():
    print(f"Scanning templates in {TEMPLATE_DIR}...")
    
    # Regex for multiline variable tags: {{ ... \n ... }}
    # We look for {{, then anything appearing (excluding }}) 
    # that contains a newline, then }}
    multiline_regex = re.compile(r'\{\{[^}]*\n[^}]*\}\}', re.MULTILINE)
    
    found_issues = False
    
    for root, dirs, files in os.walk(TEMPLATE_DIR):
        for file in files:
            if file.endswith('.html'):
                path = os.path.join(root, file)
                try:
                    with open(path, 'r', encoding='utf-8') as f:
                        content = f.read()
                        
                        matches = multiline_regex.findall(content)
                        if matches:
                            print(f"[FAIL] {file}: Found {len(matches)} multiline variable tags.")
                            found_issues = True
                            for i, match in enumerate(matches):
                                print(f"  Match {i+1}: {match.strip()[:50]}...")
                except Exception as e:
                    print(f"Error reading {file}: {e}")

    with open('verification_report.txt', 'w', encoding='utf-8') as report:
        if not found_issues:
            print("\nSUCCESS: No multiline variable tags found in any template.")
            report.write("SUCCESS: No multiline variable tags found in any template.\n")
        else:
            print("\nFAILURE: Found multiline variable tags. Please fix above files.")
            report.write("FAILURE: Found multiline variable tags. See stdout for details or checks below.\n")
            # We should probably restart logic to capture details in the file, but for now let's just use print/redirect logic or just run it and see.
            # Actually, let's just make the print statements write to file too.

def scan_templates():
    print(f"Scanning templates in {TEMPLATE_DIR}...")
    with open('verification_report.txt', 'w', encoding='utf-8') as f:
        multiline_regex = re.compile(r'\{\{[^}]*\n[^}]*\}\}', re.MULTILINE)
        found_issues = False
        
        for root, dirs, files in os.walk(TEMPLATE_DIR):
            for file in files:
                if file.endswith('.html'):
                    path = os.path.join(root, file)
                    try:
                        with open(path, 'r', encoding='utf-8') as tf:
                            content = tf.read()
                            matches = multiline_regex.findall(content)
                            if matches:
                                msg = f"[FAIL] {file}: Found {len(matches)} multiline variable tags.\n"
                                print(msg.strip())
                                f.write(msg)
                                found_issues = True
                                for i, match in enumerate(matches):
                                    detail = f"  Match {i+1}: {match.strip()[:50]}...\n"
                                    print(detail.strip())
                                    f.write(detail)
                    except Exception as e:
                        print(f"Error reading {file}: {e}")

        if not found_issues:
            f.write("SUCCESS: No multiline variable tags found.")

