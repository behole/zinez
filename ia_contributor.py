#!/usr/bin/env python3
"""
Internet Archive Contributor
Upload punk zines from other sources back to Internet Archive

This script helps contribute non-IA sourced zines TO the Internet Archive,
establishing a bidirectional workflow with IA.

Features:
- Identifies zines that need to be uploaded to IA
- Prepares metadata in IA format
- Generates upload commands
- Creates batch upload scripts
- Tracks contribution status
"""

import json
import os
import sys
from pathlib import Path
from typing import List, Dict, Optional
from datetime import datetime
import re

# Check for required libraries
try:
    from internetarchive import get_item, upload
    IA_AVAILABLE = True
except ImportError:
    print("⚠️  internetarchive library not installed")
    print("Run: pip install internetarchive")
    IA_AVAILABLE = False


class IAContributor:
    """Manage contributions of punk zines to Internet Archive"""

    def __init__(self, database_path: str = "punk_zines_database.json"):
        self.database_path = database_path
        self.database = self.load_database()
        self.contributions_dir = Path("ia_contributions")
        self.contributions_dir.mkdir(exist_ok=True)
        self.batch_scripts_dir = self.contributions_dir / "batch_scripts"
        self.batch_scripts_dir.mkdir(exist_ok=True)

    def load_database(self) -> Dict:
        """Load existing database"""
        if os.path.exists(self.database_path):
            with open(self.database_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {"database_info": {}, "zines": []}

    def save_database(self):
        """Save database to file"""
        with open(self.database_path, 'w', encoding='utf-8') as f:
            json.dump(self.database, f, indent=2, ensure_ascii=False)

    def identify_contribution_candidates(self) -> List[Dict]:
        """Find zines that should be contributed to IA"""
        candidates = []

        for zine in self.database.get('zines', []):
            source_type = zine.get('source_type', '')

            # Candidates are zines NOT from Internet Archive
            if source_type != 'internet_archive':
                # Check if they have local images or content
                image_url = zine.get('image_url', '')
                if image_url and not image_url.startswith('http'):
                    # Has local image - good candidate
                    candidates.append(zine)
                elif source_type in ['physical_collection', 'other_archive', 'personal_collection']:
                    # Explicitly marked as non-IA source
                    candidates.append(zine)

        return candidates

    def generate_ia_identifier(self, zine: Dict) -> str:
        """Generate Internet Archive identifier for zine"""
        # IA identifiers must be lowercase, no spaces, alphanumeric + - _
        zine_name = zine.get('zine_name', 'unknown')
        issue = zine.get('issue_number', '')
        year = zine.get('year', '')

        # Clean name
        clean_name = re.sub(r'[^a-zA-Z0-9\s]', '', zine_name)
        clean_name = clean_name.lower().replace(' ', '-')

        # Build identifier
        parts = ['punk-zine', clean_name]
        if issue:
            parts.append(f"issue{issue}")
        if year:
            parts.append(year)

        identifier = '-'.join(parts)

        # IA identifiers must be unique - add suffix if needed
        return identifier

    def prepare_ia_metadata(self, zine: Dict) -> Dict:
        """Prepare metadata in Internet Archive format"""
        identifier = self.generate_ia_identifier(zine)

        # Build description
        description_parts = []
        if zine.get('description'):
            description_parts.append(zine['description'])

        description_parts.append(f"\nPunk zine from {zine.get('location', 'Unknown location')}")

        if zine.get('year'):
            description_parts.append(f"Published: {zine['year']}")

        if zine.get('bands_featured'):
            bands = ', '.join(zine['bands_featured'])
            description_parts.append(f"\nFeatured bands: {bands}")

        description_parts.append("\n---")
        description_parts.append("Contributed by the Punk Zines Research Project")
        description_parts.append("Part of documenting underground punk culture and DIY publishing")

        # Prepare metadata
        metadata = {
            'title': zine.get('zine_name', 'Unknown Zine'),
            'mediatype': 'texts',
            'collection': 'opensource',  # Default collection - can be changed
            'description': '\n'.join(description_parts),
            'subject': '; '.join(zine.get('tags', ['punk', 'zine', 'fanzine'])),
            'creator': zine.get('creators', 'Unknown'),
            'date': zine.get('year', ''),
            'language': 'eng',
            'licenseurl': 'http://creativecommons.org/licenses/by-nc-sa/4.0/',
        }

        # Add optional fields
        if zine.get('location'):
            metadata['coverage'] = zine['location']

        if zine.get('issue_number'):
            metadata['volume'] = zine['issue_number']

        return identifier, metadata

    def generate_upload_script(self, zine: Dict, identifier: str, metadata: Dict) -> str:
        """Generate shell script for uploading this zine"""
        image_path = zine.get('image_url', '')

        # Build ia upload command
        script_lines = [
            "#!/bin/bash",
            "# Upload script for Internet Archive",
            f"# Zine: {zine.get('zine_name', 'Unknown')}",
            f"# Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            "",
            "# Check if internetarchive is configured",
            "if ! ia configure --help &> /dev/null; then",
            "    echo 'Error: internetarchive not configured'",
            "    echo 'Run: ia configure'",
            "    exit 1",
            "fi",
            "",
            f"# Upload {identifier}",
            "ia upload \\",
            f'  "{identifier}" \\',
        ]

        # Add file if exists
        if image_path and os.path.exists(image_path):
            script_lines.append(f'  "{image_path}" \\')

        # Add metadata
        for key, value in metadata.items():
            # Escape quotes in values
            safe_value = str(value).replace('"', '\\"')
            script_lines.append(f'  --metadata="{key}:{safe_value}" \\')

        # Remove last backslash and add closing
        script_lines[-1] = script_lines[-1].rstrip(' \\')
        script_lines.extend([
            "",
            'echo "Upload complete!"',
            f'echo "View at: https://archive.org/details/{identifier}"',
        ])

        return '\n'.join(script_lines)

    def create_contribution_package(self, zine: Dict) -> Dict:
        """Create complete contribution package for one zine"""
        identifier, metadata = self.prepare_ia_metadata(zine)

        # Generate upload script
        script_content = self.generate_upload_script(zine, identifier, metadata)

        # Save individual upload script
        script_filename = f"upload_{identifier}.sh"
        script_path = self.batch_scripts_dir / script_filename

        with open(script_path, 'w', encoding='utf-8') as f:
            f.write(script_content)

        # Make executable
        os.chmod(script_path, 0o755)

        package = {
            'zine_id': zine['id'],
            'zine_name': zine['zine_name'],
            'ia_identifier': identifier,
            'metadata': metadata,
            'upload_script': str(script_path),
            'status': 'prepared',
            'prepared_date': datetime.now().isoformat()
        }

        return package

    def prepare_all_contributions(self) -> List[Dict]:
        """Prepare all contribution packages"""
        print("=" * 70)
        print("🎸 PUNK ZINE CONTRIBUTOR - Internet Archive")
        print("=" * 70)
        print("\n📋 Identifying contribution candidates...")

        candidates = self.identify_contribution_candidates()

        if not candidates:
            print("\n✅ No new zines to contribute - all are already from IA!")
            return []

        print(f"\n📦 Found {len(candidates)} zines to contribute:")
        print("   (Zines from non-IA sources that can be uploaded)")

        packages = []

        for zine in candidates:
            print(f"\n📄 Preparing: {zine.get('zine_name', 'Unknown')}")
            print(f"   Source: {zine.get('source_type', 'unknown')}")
            print(f"   Current archive: {zine.get('archive_source', 'none')}")

            try:
                package = self.create_contribution_package(zine)
                packages.append(package)
                print(f"   ✅ Package created: {package['ia_identifier']}")
                print(f"   📜 Upload script: {package['upload_script']}")
            except Exception as e:
                print(f"   ⚠️  Error creating package: {e}")

        # Save manifest
        manifest_path = self.contributions_dir / "contribution_manifest.json"
        with open(manifest_path, 'w', encoding='utf-8') as f:
            json.dump({
                'created': datetime.now().isoformat(),
                'total_packages': len(packages),
                'packages': packages
            }, f, indent=2)

        print(f"\n✅ Manifest saved: {manifest_path}")

        # Create master upload script
        self.create_master_upload_script(packages)

        return packages

    def create_master_upload_script(self, packages: List[Dict]):
        """Create a master script to upload all zines"""
        master_script_path = self.batch_scripts_dir / "upload_all_zines.sh"

        script_lines = [
            "#!/bin/bash",
            "# Master upload script for all prepared punk zines",
            f"# Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            f"# Total zines: {len(packages)}",
            "",
            "echo '========================================='",
            "echo '🎸 Uploading Punk Zines to Internet Archive'",
            f"echo 'Total zines to upload: {len(packages)}'",
            "echo '========================================='",
            "",
            "# Check if internetarchive is configured",
            "if ! ia configure --help &> /dev/null; then",
            "    echo 'Error: internetarchive not configured'",
            "    echo 'Run: ia configure'",
            "    exit 1",
            "fi",
            "",
            "UPLOAD_COUNT=0",
            "ERROR_COUNT=0",
            "",
        ]

        for i, package in enumerate(packages, 1):
            script_lines.extend([
                f"# Upload {i}/{len(packages)}: {package['zine_name']}",
                f"echo ''",
                f"echo 'Uploading {i}/{len(packages)}: {package['zine_name']}'",
                f"if bash '{package['upload_script']}'; then",
                f"    UPLOAD_COUNT=$((UPLOAD_COUNT + 1))",
                f"    echo '✅ Success!'",
                f"else",
                f"    ERROR_COUNT=$((ERROR_COUNT + 1))",
                f"    echo '❌ Failed'",
                f"fi",
                f"",
                "# Rate limiting - be nice to IA servers",
                "sleep 5",
                "",
            ])

        script_lines.extend([
            "echo ''",
            "echo '========================================='",
            "echo '📊 Upload Summary'",
            "echo \"Successful: $UPLOAD_COUNT\"",
            "echo \"Failed: $ERROR_COUNT\"",
            "echo '========================================='",
        ])

        with open(master_script_path, 'w', encoding='utf-8') as f:
            f.write('\n'.join(script_lines))

        os.chmod(master_script_path, 0o755)

        print(f"\n🚀 Master upload script created: {master_script_path}")
        print(f"\n📝 To upload all zines to Internet Archive:")
        print(f"   1. Configure IA CLI: ia configure")
        print(f"   2. Run: bash {master_script_path}")

    def mark_as_contributed(self, zine_id: str, ia_identifier: str):
        """Mark a zine as contributed to IA"""
        for zine in self.database.get('zines', []):
            if zine['id'] == zine_id:
                zine['source_type'] = 'contributed_to_ia'
                zine['ia_item_url'] = f"https://archive.org/details/{ia_identifier}"
                zine['ia_identifier'] = ia_identifier
                zine['contribution_date'] = datetime.now().isoformat()
                break

        self.save_database()

    def show_statistics(self):
        """Show statistics about IA contributions"""
        zines = self.database.get('zines', [])

        ia_sourced = sum(1 for z in zines if z.get('source_type') == 'internet_archive')
        contributed = sum(1 for z in zines if z.get('source_type') == 'contributed_to_ia')
        other_sources = sum(1 for z in zines if z.get('source_type') not in ['internet_archive', 'contributed_to_ia', None])
        unknown = len(zines) - ia_sourced - contributed - other_sources

        print("\n" + "=" * 70)
        print("📊 DATABASE SOURCE STATISTICS")
        print("=" * 70)
        print(f"Total zines in database: {len(zines)}")
        print(f"\n📥 From Internet Archive: {ia_sourced}")
        print(f"📤 Contributed TO Internet Archive: {contributed}")
        print(f"📦 From other sources: {other_sources}")
        print(f"❓ Unknown source: {unknown}")
        print(f"\n🔄 Bidirectional coverage: {ia_sourced + contributed}/{len(zines)} ({(ia_sourced + contributed)/len(zines)*100:.1f}%)")
        print("=" * 70)


def main():
    """Main entry point"""
    print("🎸 Internet Archive Contributor - Punk Zines Project\n")

    contributor = IAContributor()

    if len(sys.argv) > 1:
        command = sys.argv[1]

        if command == "--prepare":
            # Prepare all contribution packages
            packages = contributor.prepare_all_contributions()

            if packages:
                print("\n" + "=" * 70)
                print("📦 CONTRIBUTION PACKAGES READY")
                print("=" * 70)
                print(f"Total packages: {len(packages)}")
                print(f"Location: {contributor.batch_scripts_dir}")
                print(f"\nNext steps:")
                print(f"1. Review the packages in: {contributor.contributions_dir}")
                print(f"2. Configure IA: ia configure")
                print(f"3. Upload all: bash {contributor.batch_scripts_dir}/upload_all_zines.sh")
                print("=" * 70)

        elif command == "--stats":
            # Show statistics
            contributor.show_statistics()

        elif command == "--help":
            print("""
Internet Archive Contributor
Prepare and upload punk zines to Internet Archive

Commands:
  --prepare    Prepare all non-IA zines for upload
  --stats      Show database source statistics
  --help       Show this help

Workflow:
  1. Run with --prepare to create upload packages
  2. Review generated scripts in ia_contributions/batch_scripts/
  3. Configure IA CLI: ia configure
  4. Upload using generated scripts

Examples:
  python ia_contributor.py --prepare
  python ia_contributor.py --stats
""")
        else:
            print(f"Unknown command: {command}")
            print("Use --help for usage information")

    else:
        # Default: show stats
        contributor.show_statistics()
        print("\nUse --prepare to create contribution packages")
        print("Use --help for more options")


if __name__ == "__main__":
    main()
