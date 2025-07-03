#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import click
import os
import httpx
import pyquery
from loguru import logger
from typing import List
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass

@dataclass(frozen=True)
class Faculty:
    name: str
    bio: str
    discipline: str

    def greeting(self) -> str:
        return f"Hello, my name is {self.name} and I am a {self.discipline} faculty member."



def find_economists(faculties: list[Faculty]) -> list[Faculty]:
    return [faculty for faculty in faculties if "econ" in faculty.discipline.lower()]  

@click.group()
def cli() -> None:
    pass

def fetch_faculty_bio(slug: str) -> str:
    url = f"https://som.yale.edu/faculty-research/faculty-directory/{slug}"
    response = httpx.get(url)
    response.raise_for_status()
    return response.text

def parse_faculty_bio(html: str) -> Faculty:
    doc = pyquery.PyQuery(html)
    name = doc('.node__title').text()
    bio = doc('.text__body').eq(0).text()
    discipline = doc('.node__discipline p').text()
    return Faculty(name=name, bio=bio, discipline=discipline)

@cli.command()
@click.argument('slug', type=str)
def fetch_bio(slug: str) -> None:
    html = fetch_faculty_bio(slug)
    person = parse_faculty_bio(html)
    print(person)

@cli.command()
@click.argument('input_file', type=str)
@click.argument('output_directory', type=str)
def download_profiles(input_file: str, output_directory: str) -> None:
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)
    
    slugs = [line.strip() for line in open(input_file, 'r') if line.strip()]
    with ThreadPoolExecutor(max_workers=5) as executor:
        futures = {executor.submit(fetch_faculty_bio, slug): slug for slug in slugs}
        for future in as_completed(futures):
            slug = futures[future]
            try:
                html = future.result()
                person = parse_faculty_bio(html)
                output_file = os.path.join(output_directory, f"{slug}.txt")
                with open(output_file, 'w') as f:
                    f.write(f"Name: {person.name}\nBio: {person.bio}\nDiscipline: {person.discipline}\n")
                logger.info(f"Downloaded profile for {slug} to {output_file}")
            except Exception as e:
                logger.error(f"Error fetching profile for {slug}: {e}")

@cli.command()
@click.argument('input_files', type=str, nargs=-1)
def fetch_all_economists(input_files: list[str]) -> None:
    faculty = []
    bios = [open(file, 'r').read() for file in input_files]
    faculty = [parse_faculty_bio(bio) for bio in bios if bio.strip()]
    economists = find_economists(faculty)
    for economist in economists:
        print(economist)

@cli.command()
@click.argument('department', type=str)
@click.argument('years_at_yale', type=int)
def say_hello(department: str, years_at_yale: int) -> None:
    bio = f"An economist with a focus on macroeconomics who has been at Yale for {years_at_yale} years."
    kyle = Faculty("Kyle", bio, department)
    print(kyle)

@cli.command()
def print_seminar_schedule():
    print("Seminar Schedule:")
    print("1. Macroeconomics Seminar - Mondays at 10 AM")
    print("2. Microeconomics Seminar - Wednesdays at 2 PM")
    print("3. Econometrics Seminar - Fridays at 1 PM")

@cli.command()
@click.argument('input_files', type=str, nargs=-1)
def find_most_verbose_bio(input_files: List[str]) -> None:
    # Open files, parse bios to faculty and see which
    # has the most words in their bio
    if not input_files:
        logger.error(f"No input files provided.")
        return
    htmls = [open(file, 'r').read() for file in input_files]
    faculties = [parse_faculty_bio(html) for html in htmls if html.strip()]
    print(faculties)
    most_verbose_person = max(faculties, key=lambda f: len(f.bio.split()))
    print(f"Most verbose bio: {most_verbose_person.name} with {len(most_verbose_person.bio.split())} words.")

if __name__ == "__main__":
    cli()