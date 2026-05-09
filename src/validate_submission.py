#!/usr/bin/env python3
"""Course-modified validator for the C146 ARSA SNV submission file.

Usage:
    python s26-c146-arsa-cagi-snv-validation.py submission.tsv s26-c146-arsa-cagi-snv-template.tsv

Behavior:
- validates against the course SNV template (not the full public challenge list)
- accepts a literal '*' in the SD column
- requires the header: aa_substitution\tstability_score_48hr\tsd\tcomment
"""
import csv
import os
import re
import sys

EXPECTED_HEADER = ['aa_substitution', 'stability_score_48hr', 'sd', 'comment']
VARIANT_RE = re.compile(r'^[A-Z][0-9]+[A-Z]$')


def load_expected_variants(template_path):
    if not os.path.exists(template_path):
        raise FileNotFoundError(f'Template file not found: {template_path}')
    expected = []
    with open(template_path, 'r', newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f, delimiter='\t')
        if reader.fieldnames != EXPECTED_HEADER:
            raise ValueError(f'Template header mismatch. Expected {EXPECTED_HEADER}, found {reader.fieldnames}')
        for row in reader:
            aa = (row.get('aa_substitution') or '').strip()
            if aa:
                expected.append(aa)
    return expected


def main():
    if len(sys.argv) != 3:
        print('Usage: python s26-c146-arsa-cagi-snv-validation.py <submission.tsv> <template.tsv>')
        sys.exit(2)
    submission_path = sys.argv[1]
    template_path = sys.argv[2]
    expected = load_expected_variants(template_path)
    expected_set = set(expected)
    if not os.path.exists(submission_path):
        print(f'Error: submission file not found: {submission_path}')
        sys.exit(2)
    errors = []
    warnings = []
    submitted = []
    submitted_set = set()
    with open(submission_path, 'r', newline='', encoding='utf-8') as f:
        reader = csv.reader(f, delimiter='\t')
        try:
            header = next(reader)
        except StopIteration:
            print('Error: submission file is empty')
            sys.exit(2)
        if header != EXPECTED_HEADER:
            warnings.append(f'Header mismatch. Expected {EXPECTED_HEADER}, found {header}')
        for lineno, parts in enumerate(reader, start=2):
            if not parts or all(p == '' for p in parts):
                continue
            while len(parts) < 4:
                parts.append('')
            aa, score, sd, comment = parts[0].strip(), parts[1].strip(), parts[2].strip(), parts[3]
            if not VARIANT_RE.match(aa):
                errors.append(f'line {lineno}: invalid aa_substitution format: {aa!r}')
                continue
            if aa not in expected_set:
                errors.append(f'line {lineno}: variant not found in template: {aa}')
                continue
            if aa in submitted_set:
                errors.append(f'line {lineno}: duplicate variant in submission: {aa}')
                continue
            submitted.append(aa)
            submitted_set.add(aa)
            try:
                score_val = float(score)
            except Exception:
                errors.append(f'line {lineno}: invalid stability_score_48hr value: {score!r}')
                continue
            if not (0.0 <= score_val <= 1.0):
                errors.append(f'line {lineno}: stability_score_48hr must be between 0 and 1 inclusive; found {score_val}')
            if sd != '*':
                try:
                    sd_val = float(sd)
                except Exception:
                    errors.append(f'line {lineno}: invalid sd value: {sd!r}; must be nonnegative float or *')
                    continue
                if sd_val < 0:
                    errors.append(f'line {lineno}: sd must be nonnegative; found {sd_val}')
    missing = [aa for aa in expected if aa not in submitted_set]
    print(f'Expected variants: {len(expected)}')
    print(f'Submitted variants: {len(submitted)}')
    print(f'Missing variants: {len(missing)}')
    print(f'Warnings: {len(warnings)}')
    print(f'Errors: {len(errors)}')
    if warnings:
        print('\n=== WARNINGS ===')
        for w in warnings:
            print(w)
    if errors:
        print('\n=== ERRORS ===')
        for e in errors[:200]:
            print(e)
        if len(errors) > 200:
            print(f'... {len(errors)-200} additional errors omitted ...')
        sys.exit(1)
    if missing:
        print('\n=== MISSING VARIANTS ===')
        for aa in missing[:200]:
            print(aa)
        if len(missing) > 200:
            print(f'... {len(missing)-200} additional missing variants omitted ...')
        sys.exit(1)
    print("\nThe file's format is valid and complete! You are good to submit now!")

if __name__ == '__main__':
    main()
