from __future__ import annotations

import re

import pytest
from playwright.sync_api import Page, expect


class TestPageLoads:
    def test_page_title(self, live_page: Page):
        expect(live_page).to_have_title(re.compile(r"Wedding Planner"))

    def test_header_kicker(self, live_page: Page):
        expect(live_page.get_by_text("LangChain portfolio project")).to_be_visible()

    def test_header_title(self, live_page: Page):
        expect(live_page.get_by_text("Multi-Agent Wedding Planner").first).to_be_visible()

    def test_header_subtitle(self, live_page: Page):
        expect(
            live_page.get_by_text("Build a client-ready planning brief")
        ).to_be_visible()

    def test_header_chips(self, live_page: Page):
        for chip in ["9-agent flow", "Venue research", "Budget optimization",
                      "Timeline planning", "Design direction"]:
            expect(live_page.locator(f".header-chip:has-text('{chip}')")).to_be_visible()


class TestDashboardCards:
    def test_runtime_card(self, live_page: Page):
        expect(live_page.locator(".summary-card .label:has-text('Runtime')")).to_be_visible()

    def test_event_date_card(self, live_page: Page):
        expect(live_page.locator(".summary-card .label:has-text('Event Date')")).to_be_visible()

    def test_budget_card(self, live_page: Page):
        expect(live_page.locator(".summary-card .label:has-text('Budget')")).to_be_visible()

    def test_planning_focus_card(self, live_page: Page):
        expect(live_page.locator(".summary-card .label:has-text('Planning Focus')")).to_be_visible()


class TestFormElements:
    def test_form_title(self, live_page: Page):
        expect(live_page.get_by_text("Wedding Brief", exact=True)).to_be_visible()

    def test_couple_name_input(self, live_page: Page):
        expect(live_page.get_by_text("Couple or project name")).to_be_visible()

    def test_location_input(self, live_page: Page):
        expect(live_page.locator('[data-testid="stForm"]').get_by_text("Location", exact=True)).to_be_visible()

    def test_guest_count_input(self, live_page: Page):
        expect(live_page.get_by_text("Guest count", exact=True)).to_be_visible()

    def test_date_input(self, live_page: Page):
        expect(live_page.get_by_text("Target date")).to_be_visible()

    def test_currency_select(self, live_page: Page):
        expect(live_page.get_by_text("Currency", exact=True).first).to_be_visible()

    def test_budget_slider(self, live_page: Page):
        expect(live_page.locator('[data-testid="stForm"]').get_by_text("Budget range")).to_be_visible()

    def test_tone_select(self, live_page: Page):
        expect(live_page.get_by_text("Planner tone")).to_be_visible()

    def test_style_multiselect(self, live_page: Page):
        expect(live_page.locator('[data-testid="stForm"]').get_by_text("Style direction")).to_be_visible()

    def test_priority_multiselect(self, live_page: Page):
        expect(live_page.locator('[data-testid="stForm"]').get_by_text("Planning priorities")).to_be_visible()

    def test_must_haves_textarea(self, live_page: Page):
        expect(live_page.get_by_text("Must-haves", exact=True).first).to_be_visible()

    def test_constraints_textarea(self, live_page: Page):
        expect(live_page.locator('[data-testid="stForm"]').get_by_text("Constraints")).to_be_visible()

    def test_traditions_textarea(self, live_page: Page):
        expect(live_page.get_by_text("Traditions and family details")).to_be_visible()


class TestSubmitButton:
    def test_submit_button_disabled_without_keys(self, live_page: Page):
        btn = live_page.locator('[data-testid="stForm"] button:has-text("Generate wedding plan")')
        expect(btn).to_be_visible()
        expect(btn).to_be_disabled()


class TestSidebar:
    def test_sidebar_runtime_header(self, live_page: Page):
        expect(live_page.locator('[data-testid="stSidebar"]').get_by_text("Runtime").first).to_be_visible()

    def test_sidebar_groq_key_input(self, live_page: Page):
        expect(live_page.locator('[data-testid="stSidebar"]').get_by_text("Groq API key")).to_be_visible()

    def test_sidebar_tavily_key_input(self, live_page: Page):
        expect(live_page.locator('[data-testid="stSidebar"]').get_by_text("Tavily API key")).to_be_visible()

    def test_sidebar_key_badges(self, live_page: Page):
        expect(live_page.locator('[data-testid="stSidebar"]').locator(".badge")).to_have_count(2)

    def test_sidebar_demo_controls(self, live_page: Page):
        expect(live_page.locator('[data-testid="stSidebar"]').get_by_text("Demo Controls")).to_be_visible()

    def test_sidebar_load_sample_button(self, live_page: Page):
        expect(live_page.locator('[data-testid="stSidebar"]').get_by_text("Load sample brief")).to_be_visible()

    def test_sidebar_agents_list(self, live_page: Page):
        expect(live_page.locator('[data-testid="stSidebar"]').get_by_text("Agents")).to_be_visible()
        for agent in ["VenueAgent", "CateringAgent", "PhotographyAgent",
                       "BudgetAgent", "DesignAgent", "TimelineAgent",
                       "TravelAgent", "GuestAgent"]:
            expect(live_page.locator(f'[data-testid="stSidebar"] p:has-text("{agent}")')).to_be_visible()


class TestPlanningLens:
    def test_planning_lens_header(self, live_page: Page):
        expect(live_page.locator(".side-panel h3:has-text('Planning Lens')")).to_be_visible()


class TestAgentFlow:
    def test_agent_flow_header(self, live_page: Page):
        expect(live_page.locator(".side-panel h3:has-text('Agent Flow')")).to_be_visible()

    def test_main_agent_in_flow(self, live_page: Page):
        expect(live_page.locator(".side-panel strong:has-text('MainWeddingPlannerAgent')")).to_be_visible()


class TestResultsSection:
    def test_results_section_title(self, live_page: Page):
        expect(live_page.locator(".section-label:has-text('Latest Output')")).to_be_visible()

    def test_empty_state(self, live_page: Page):
        expect(live_page.get_by_text("No plan generated yet")).to_be_visible()


class TestKeyOverrideWorkflow:
    def test_entering_keys_enables_button(self, live_page: Page):
        sidebar = live_page.locator('[data-testid="stSidebar"]')
        groq_input = sidebar.locator("input[type='password']").first
        groq_input.click()
        groq_input.type("gsk_test_key_12345", delay=20)
        groq_input.press("Enter")
        live_page.wait_for_selector('[data-testid="stSidebar"] .badge-ready', timeout=10000)
        tavily_input = sidebar.locator("input[type='password']").nth(1)
        tavily_input.click()
        tavily_input.type("tvly_test_key_12345", delay=20)
        tavily_input.press("Enter")
        live_page.wait_for_timeout(5000)
        btn = live_page.locator('[data-testid="stForm"] button:has-text("Generate wedding plan")')
        expect(btn).to_be_enabled()


class TestSampleBriefLoading:
    def test_load_sample_fills_form(self, live_page: Page):
        sidebar = live_page.locator('[data-testid="stSidebar"]')
        sidebar.get_by_text("Load sample brief").click()
        live_page.wait_for_timeout(3000)
        form = live_page.locator('[data-testid="stForm"]')
        couple_input = form.locator("input[type='text']").first
        expect(couple_input).to_have_value("Amira and Noah")
