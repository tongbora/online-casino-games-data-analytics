"""
dashboard/pages/about_author.py
──────────────────────────────
Page: About the Authors
Two editable team-member cards for the sidebar navigation.
"""

import base64
from pathlib import Path

import streamlit as st


ROOT = Path(__file__).resolve().parents[2]
DORN_DANA_PHOTO = ROOT / 'assets' / 'dorn_dana.jpg'
TONG_BORA_PHOTO = ROOT / 'assets' / 'tong_bora.jpg'


TEAM_MEMBERS = [
    {
        'initials': 'A2',
        'name': 'Dorn Dana',
        'role': 'Leader',
        'bio': 'Be the change that you wish to see in the world.',
        'image_path': DORN_DANA_PHOTO,
    },
    {
        'initials': 'A1',
        'name': 'Tong Bora',
        'role': 'Team Member',
        'bio': "If you tell the truth, you don't have to remember anything.",
        'image_path': TONG_BORA_PHOTO,
    }
]


def _image_to_data_uri(image_path: Path | None) -> str | None:
    if not image_path or not image_path.exists():
        return None
    encoded = base64.b64encode(image_path.read_bytes()).decode('utf-8')
    return f'data:image/jpeg;base64,{encoded}'


def _render_team_card(member: dict[str, object]) -> str:
    image_uri = _image_to_data_uri(member.get('image_path'))
    avatar = (
        f'<img class="team-photo" src="{image_uri}" alt="{member["name"]}" />'
        if image_uri
        else f'<div class="team-avatar">{member["initials"]}</div>'
    )
    return f'''
<div class="team-card">
    <div class="team-photo-wrap">{avatar}</div>
    <div class="team-content">
        <div class="team-name">{member['name']}</div>
        <p class="team-role">{member['role']}</p>
        <p class="team-bio">{member['bio']}</p>
    </div>
</div>
'''


def render() -> None:
    st.title('About the Authors')
    st.markdown('Get to know the authors and their responsibilities in developing this project.')
    st.markdown(
        '<div class="team-grid">' + ''.join(_render_team_card(member) for member in TEAM_MEMBERS) + '</div>',
        unsafe_allow_html=True,
    )

    # st.markdown('### Update me')
    # st.markdown(
    #     '- Replace the names and initials\n'
    #     '- Add short bios or role descriptions\n'
    #     '- Add links or photos later if needed'
    # )