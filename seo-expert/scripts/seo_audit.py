import os
import re
import sys

def audit_file(file_path):
    issues = []
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
        
    # Check for Metadata API usage in pages/roots
    if 'layout.tsx' in file_path or 'page.tsx' in file_path:
        if 'export const metadata' not in content and 'generateMetadata' not in content:
            issues.append("[METADATA] Missing 'metadata' or 'generateMetadata' export.")

    # Check for multiple H1s
    h1_count = len(re.findall(r'<h1', content, re.IGNORECASE))
    if h1_count > 1:
        issues.append(f"[SEO] Multiple H1 tags found ({h1_count}). Only one H1 per page is recommended.")
    elif h1_count == 0 and 'page.tsx' in file_path:
        issues.append("[SEO] No H1 tag found. Each page should have exactly one H1.")

    # Check for missing alt tags in images
    # This is a rough regex check for <img tags without alt
    img_tags = re.findall(r'<img[^>]*>', content, re.IGNORECASE)
    for img in img_tags:
        if 'alt=' not in img.lower():
            issues.append(f"[ACCESSIBILITY] Image tag missing 'alt' attribute: {img[:50]}...")

    # Check for hardcoded meta tags (Next.js discourages these in favor of Metadata API)
    if '<meta' in content and ('layout.tsx' in file_path or 'page.tsx' in file_path):
        issues.append("[OPTIMIZATION] Found hardcoded <meta> tags. Recommended to move to Next.js Metadata API.")

    return issues

def main(directory):
    print(f"--- SEO Audit Report for: {directory} ---")
    total_issues = 0
    for root, _, files in os.walk(directory):
        if 'node_modules' in root or '.next' in root:
            continue
        for file in files:
            if file.endswith(('.tsx', '.jsx', '.html')):
                path = os.path.join(root, file)
                file_issues = audit_file(path)
                if file_issues:
                    print(f"\nFile: {os.path.relpath(path, directory)}")
                    for issue in file_issues:
                        print(f"  - {issue}")
                        total_issues += 1
    
    print(f"\n--- Total SEO/Accessibility Issues Found: {total_issues} ---")

if __name__ == "__main__":
    target_dir = sys.argv[1] if len(sys.argv) > 1 else "."
    main(target_dir)
