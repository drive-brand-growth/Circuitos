#!/usr/bin/env python3
"""
Circuit OS Icon Replacement Script
Replaces all generic emojis with custom Circuit OS SVG icons
"""

import re
import os
from pathlib import Path

# Define emoji to icon mappings
EMOJI_MAPPINGS = {
    # Primary brand icons
    '⚡': 'icon-circuit-bolt',

    # Data and analytics
    '📊': 'icon-analytics',
    '📈': 'icon-chart-up',
    '📉': 'icon-chart-down',

    # Status and checks
    '✅': 'icon-check-circle',
    '✓': 'icon-check-circle',
    '⚠️': 'icon-alert',
    '⚠': 'icon-alert',
    '❗': 'icon-alert',
    '✗': 'icon-alert',
    '🚫': 'icon-alert',

    # Users and team
    '👤': 'icon-user',
    '👥': 'icon-team',

    # Decision and targets
    '🎯': 'icon-decision',

    # Business
    '🏢': 'icon-building',
    '💰': 'icon-money',
    '🏭': 'icon-industry',

    # AI and processing
    '🤖': 'icon-processing',
    '🧠': 'icon-brain',
    '🔄': 'icon-refresh',
    '⚙️': 'icon-processing',
    '⚙': 'icon-processing',

    # Communication
    '📧': 'icon-outreach',
    '✉️': 'icon-outreach',
    '✉': 'icon-outreach',
    '📨': 'icon-outreach',
    '📩': 'icon-outreach',

    # Files and data
    '📂': 'icon-upload',
    '📁': 'icon-upload',
    '📥': 'icon-data-input',
    '📝': 'icon-data-input',
    '📋': 'icon-copy',

    # Security and governance
    '🛡️': 'icon-shield',
    '🛡': 'icon-shield',
    '🔒': 'icon-lock',
    '⚖️': 'icon-balance',
    '⚖': 'icon-balance',

    # Architecture and tools
    '🏗️': 'icon-architecture',
    '🏗': 'icon-architecture',
    '🔧': 'icon-tools',
    '🔨': 'icon-tools',

    # Technology
    '🐍': 'icon-code',
    '🌐': 'icon-web',
    '💻': 'icon-code',
    '🖥️': 'icon-dashboard',
    '🖥': 'icon-dashboard',
    '📱': 'icon-dashboard',

    # Value and success
    '💎': 'icon-diamond',
    '🎓': 'icon-education',
    '🚀': 'icon-rocket',
    '🎨': 'icon-diamond',

    # Cycle and refresh
    '🔁': 'icon-refresh',
    '🔃': 'icon-refresh',

    # Links
    '🔗': 'icon-link',
}

def create_svg_icon(icon_id, size='', extra_classes=''):
    """Create an SVG icon HTML snippet"""
    classes = f'circuit-icon {size} {extra_classes}'.strip()
    return f'<svg class="{classes}"><use href="../circuit-icons.svg#{icon_id}"/></svg>'

def replace_emoji_in_content(content, filepath):
    """Replace emojis with SVG icons in HTML content"""

    # Determine path prefix based on file location
    if 'Dashboards' in str(filepath):
        path_prefix = '../'
    else:
        path_prefix = ''

    # Replace emojis in different contexts
    for emoji, icon_id in EMOJI_MAPPINGS.items():
        # Pattern 1: Emoji in stat-icon divs
        pattern1 = f'<div class="stat-icon">{emoji}</div>'
        replacement1 = f'''<div class="stat-icon">
                            <svg class="circuit-icon large active">
                                <use href="{path_prefix}circuit-icons.svg#{icon_id}"/>
                            </svg>
                        </div>'''
        content = content.replace(pattern1, replacement1)

        # Pattern 2: Emoji in card-icon divs
        pattern2 = f'<div class="card-icon">{emoji}</div>'
        replacement2 = f'''<div class="card-icon">
                            <svg class="circuit-icon active">
                                <use href="{path_prefix}circuit-icons.svg#{icon_id}"/>
                            </svg>
                        </div>'''
        content = content.replace(pattern2, replacement2)

        # Pattern 3: Emoji in feature-icon spans
        pattern3 = f'<span class="feature-icon">{emoji}</span>'
        replacement3 = f'<svg class="circuit-icon small active" style="margin-right: 8px;"><use href="{path_prefix}circuit-icons.svg#{icon_id}"/></svg>'
        content = content.replace(pattern3, replacement3)

        # Pattern 4: Emoji in stage-icon divs (already done for some files)
        pattern4 = f'<div class="stage-icon">{emoji}</div>'
        replacement4 = f'''<div class="stage-icon">
                            <svg class="circuit-icon large">
                                <use href="{path_prefix}circuit-icons.svg#{icon_id}"/>
                            </svg>
                        </div>'''
        content = content.replace(pattern4, replacement4)

        # Pattern 5: Emoji in architecture titles
        pattern5 = f'<div class="architecture-title">{emoji} '
        replacement5 = f'''<div class="architecture-title">
                            <svg class="circuit-icon" style="margin-right: 8px;">
                                <use href="{path_prefix}circuit-icons.svg#{icon_id}"/>
                            </svg>
                            '''
        content = content.replace(pattern5, replacement5)

        # Pattern 6: Emoji in recommendation titles
        pattern6 = f'<div class="recommendation-title">{emoji} '
        replacement6 = f'''<div class="recommendation-title">
                            <svg class="circuit-icon small active" style="margin-right: 6px;">
                                <use href="{path_prefix}circuit-icons.svg#{icon_id}"/>
                            </svg>
                            '''
        content = content.replace(pattern6, replacement6)

        # Pattern 7: Emoji in section titles
        pattern7 = f'<div class="section-title">{emoji} '
        replacement7 = f'''<div class="section-title">
                            <svg class="circuit-icon" style="margin-right: 6px;">
                                <use href="{path_prefix}circuit-icons.svg#{icon_id}"/>
                            </svg>
                            '''
        content = content.replace(pattern7, replacement7)

        # Pattern 8: Emoji in factor-name spans
        pattern8 = f'<span class="factor-name">{emoji} '
        replacement8 = f'''<span class="factor-name">
                            <svg class="circuit-icon small active" style="margin-right: 4px;">
                                <use href="{path_prefix}circuit-icons.svg#{icon_id}"/>
                            </svg>
                            '''
        content = content.replace(pattern8, replacement8)

    return content

def process_html_file(filepath):
    """Process a single HTML file"""
    print(f"Processing: {filepath}")

    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    original_content = content
    content = replace_emoji_in_content(content, filepath)

    if content != original_content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"  ✓ Updated {filepath}")
        return True
    else:
        print(f"  - No changes needed for {filepath}")
        return False

def main():
    """Main execution"""
    base_dir = Path('/Users/noelpena/Desktop/CircuitOS-DEPLOY-PACKAGE')

    # Find all HTML files
    html_files = list(base_dir.glob('**/*.html'))

    print(f"Found {len(html_files)} HTML files to process\n")

    updated_count = 0
    for filepath in html_files:
        if process_html_file(filepath):
            updated_count += 1

    print(f"\n✓ Complete! Updated {updated_count} files")

if __name__ == '__main__':
    main()
