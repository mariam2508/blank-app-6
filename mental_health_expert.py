#!/usr/bin/env python
# coding: utf-8

# In[1]:


from experta import *
from collections.abc import Mapping


# In[2]:


class MentalHealthExpert(KnowledgeEngine):
    def __init__(self):
        super().__init__()
        self.diagnoses = []

    def ask_question(self, prompt):
        while True:
            response = input(prompt).strip().lower()
            if response in ["yes", "no"]:
                return response
            print("⚠️  Please answer with 'yes' or 'no'.")

    @DefFacts()
    def _initial_action(self):
        print("\n🧠 Welcome to the Mental Wellness Expert System!")
        print("I'll ask you questions to help assess your mental health.")
        print("Please answer with 'yes' or 'no'.\n")
        yield Fact(action="assess_mental_health")

    # ===================== Symptom Collection =====================
    @Rule(Fact(action='assess_mental_health'), NOT(Fact(feeling_down=W())))
    def symptom_1(self):
        self.declare(Fact(feeling_down=self.ask_question("1. Do you often feel down, depressed, or hopeless? ")))

    @Rule(Fact(action='assess_mental_health'), NOT(Fact(loss_interest=W())))
    def symptom_2(self):
        self.declare(Fact(loss_interest=self.ask_question("2. Have you lost interest in daily activities? ")))

    @Rule(Fact(action='assess_mental_health'), NOT(Fact(sleep_issues=W())))
    def symptom_3(self):
        self.declare(Fact(sleep_issues=self.ask_question("3. Do you have significant sleep problems? ")))

    @Rule(Fact(action='assess_mental_health'), NOT(Fact(energy_loss=W())))
    def symptom_4(self):
        self.declare(Fact(energy_loss=self.ask_question("4. Do you often feel fatigued or low-energy? ")))

    @Rule(Fact(action='assess_mental_health'), NOT(Fact(anxiety=W())))
    def symptom_5(self):
        self.declare(Fact(anxiety=self.ask_question("5. Do you experience excessive anxiety or worry? ")))

    @Rule(Fact(action='assess_mental_health'), NOT(Fact(panic_attacks=W())))
    def symptom_6(self):
        self.declare(Fact(panic_attacks=self.ask_question("6. Have you had sudden panic attacks? ")))

    @Rule(Fact(action='assess_mental_health'), NOT(Fact(social_avoidance=W())))
    def symptom_7(self):
        self.declare(Fact(social_avoidance=self.ask_question("7. Do you avoid social interactions? ")))

    @Rule(Fact(action='assess_mental_health'), NOT(Fact(trauma_history=W())))
    def symptom_8(self):
        self.declare(Fact(trauma_history=self.ask_question("8. Have you experienced traumatic events? ")))

    @Rule(Fact(action='assess_mental_health'), NOT(Fact(compulsive_behavior=W())))
    def symptom_9(self):
        self.declare(Fact(compulsive_behavior=self.ask_question("9. Do you repeat rituals to reduce anxiety? ")))

    @Rule(Fact(action='assess_mental_health'), NOT(Fact(mood_swings=W())))
    def symptom_10(self):
        self.declare(Fact(mood_swings=self.ask_question("10. Do you experience extreme mood swings? ")))

    # ===================== Diagnosis Rules =====================
    @Rule(
        Fact(feeling_down="yes"),
        Fact(loss_interest="yes"),
        Fact(energy_loss="yes"),
        Fact(sleep_issues="yes")
    )
    def major_depression(self):
        self.diagnoses.append(("Major Depressive Disorder", "Moderate"))

    @Rule(
        Fact(feeling_down="yes"),
        Fact(anxiety="yes"),
        Fact(panic_attacks="yes"),
        Fact(sleep_issues="yes")
    )
    def panic_disorder(self):
        self.diagnoses.append(("Panic Disorder", "Severe"))

    @Rule(
        Fact(anxiety="yes"),
        Fact(social_avoidance="yes"),
        Fact(panic_attacks="no")
    )
    def social_anxiety(self):
        self.diagnoses.append(("Social Anxiety Disorder", "Moderate"))

    @Rule(
        Fact(trauma_history="yes"),
        Fact(sleep_issues="yes"),
        Fact(anxiety="yes")
    )
    def ptsd(self):
        self.diagnoses.append(("Post-Traumatic Stress Disorder", "Severe"))

    @Rule(
        Fact(compulsive_behavior="yes"),
        Fact(anxiety="yes"),
        Fact(feeling_down="no")
    )
    def ocd(self):
        self.diagnoses.append(("Obsessive-Compulsive Disorder", "Moderate"))

    @Rule(
        Fact(mood_swings="yes"),
        Fact(energy_loss="yes"),
        Fact(sleep_issues="yes")
    )
    def bipolar(self):
        self.diagnoses.append(("Bipolar Disorder", "Severe"))

    @Rule(
        Fact(feeling_down="yes"),
        Fact(sleep_issues="yes"),
        Fact(energy_loss="yes"),
        Fact(anxiety="no")
    )
    def seasonal_depression(self):
        self.diagnoses.append(("Seasonal Affective Disorder", "Mild"))

    # ===================== Result Synthesis =====================
    @Rule(Fact(action='assess_mental_health'), salience=-1000)
    def show_results(self):
        print("\n\n📊 Analysis Complete")
        print("====================")
        
        if not self.diagnoses:
            print("\n🌟 No clinical conditions detected")
            print("Maintain your mental wellness through regular self-care!")
        else:
            print("\n🩺 Potential Diagnoses:")
            for condition, severity in self.diagnoses:
                print(f"• {condition} ({severity} Severity)")
            
            print("\n🚑 Crisis Alert:")
            if any(sev == "Severe" for (_, sev) in self.diagnoses):
                print("Immediate professional consultation required!")
                print("🔔 National Suicide Prevention Lifeline: 1-800-273-TALK")
            else:
                print("No immediate crisis detected - monitor symptoms")
            
            print("\n💡 Recommended Actions:")
            if any(sev == "Severe" for (_, sev) in self.diagnoses):
                print("- Emergency psychiatric evaluation")
                print("- Contact crisis intervention services")
            elif any(sev == "Moderate" for (_, sev) in self.diagnoses):
                print("- Schedule therapist appointment within 2 weeks")
                print("- Start mood tracking journal")
            else:
                print("- Consider self-help strategies")
                print("- Monthly mental health check-ins")

            print("\n🔍 Condition-Specific Guidance:")
            for condition, _ in self.diagnoses:
                if "Depressive" in condition:
                    print(f"- {condition}: Regular exercise & sunlight exposure")
                if "Anxiety" in condition:
                    print(f"- {condition}: Breathing exercises & caffeine reduction")
                if "PTSD" in condition:
                    print(f"- {condition}: Trauma-focused therapy recommended")

        print("\n⚠️ Remember: This assessment isn't a replacement for professional diagnosis")

# ===================== Execution =====================
if __name__ == "__main__":
    expert = MentalHealthExpert()
    while True:
        expert.reset()
        expert.run()
        repeat = input("\n🔁 Perform another assessment? (yes/no): ").lower()
        if repeat != "yes":
            print("\n💚 Thank you for prioritizing your mental health!")
            break

