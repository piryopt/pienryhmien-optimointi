# User Guide

1. Creating a Survey
2. Creating a Multi-Stage Survey
3. Managing a Survey
4. Processing Responses
5. Answering a Survey
6. Answering a Multi-Stage Survey

The Jakaja functionalities are shown on the front page as follows:

<img src="images/front_page.png" alt="Front page" class="md-image" />

## 1. Creating a Survey

Creating a survey starts by clicking the **“Create new survey”** button on the front page. The application opens a form, which is filled in as follows:

### 1.1 Survey Name

- Give the survey a clear and descriptive name. The name must be at least 5 characters long.
- The name must be unique, as Jakaja cannot have multiple surveys with the same name running at the same time.

### 1.2 Response Period

- Set the start and end time for the survey. Click the field and select a date from the calendar or enter it in the format dd.mm.yyyy. Set the time in the format hh:mm.
- **Note:** the survey end time cannot be in the past.
- The application automatically closes the survey at the specified end time. If necessary, the survey can be reopened later (see section 3.3).

<img src="images/date_of_closing.png" alt="Date of closing" class="md-image" />

### 1.3 Survey Description

- The description is optional. You can write a short description of the survey or provide additional instructions for respondents.

<img src="images/description.png" alt="Survey description" class="md-image" />

### 1.4 Is Ranking of All Groups Required?

- Select **“Yes”** if respondents must rank all available options.
- Select **“No”** if respondents only need to rank some of the options. A new field **“Minimum number of prioritized groups”** will appear, where you can define the minimum number as an integer.

<img src="images/number_of_prioritized_groups.png" alt="Minimum prioritized groups" class="md-image" />

- Limiting the number of ranked options is recommended when there are many options (20+).
  - **NOTE:** For successful group allocation, it is important to collect sufficient preference data. Do not set the minimum number too low. It is recommended to require ranking at least 3–5 options depending on the total number of options.

### 1.5 Are Denied Choices Allowed?

- Select **“Yes”** if respondents are allowed to explicitly deny certain options. A new field **“Number of allowed denied groups”** will appear, where you can define the number of denials as an integer.
- Denying an option requires a justification of at least 10 characters, which will be visible in the response summary.

<img src="images/allow_denied_choices.png" alt="Denied choices" class="md-image" />

### 1.6 Prioritized Groups

- Options can be added manually or imported from a CSV file.
- Prioritized groups are the options respondents can rank, and into which they will be assigned after the survey closes.
- Each option must include at least:
  - Name
  - Maximum capacity
  - Minimum size (enter 0 if minimum size does not matter)
- Groups that do not meet the minimum size are excluded from allocation. To ensure a group is created regardless, select **“Force minimum size”**.
- Additional data fields can be added by clicking **“+ Add data field”**.
  - If a field should not be visible to respondents, add an asterisk (\*) to its identifier.
  - Additional fields can be removed using the trash icon.

Example with postal code and address as additional information:

<img src="images/survey_choices.png" alt="Survey choices" class="md-image" />

When a respondent opens the form, the options appear as follows:

<img src="images/answer_page.png" alt="Answer page" class="md-image" />

### Importing Options from a CSV File

- CSV is a text-based file format where values are separated by commas.  
  ([More information on Wikipedia](https://en.wikipedia.org/wiki/Comma-separated_values))
- Detailed instructions for importing options from a CSV file can be found here: [csv-instructions](csv-instructions)

### Create Survey

- Once all required fields are filled in, click **“Create survey”**.
- If creation fails, the application displays an error message describing what needs to be fixed.
- The survey appears on the **“View previous surveys”** page and under **“Active surveys”** on the front page.

---

## 2. Creating a Multi-Stage Survey

Creating a multi-stage survey starts in the same way as a regular survey, but the form includes additional settings:

### 2.1 Are Absences Allowed?

- Select **“Yes”** if respondents are allowed to mark themselves as absent.
  - Absences are then allowed in all stages.

### 2.2 Limit Participation Count

- Select **“Yes”** to limit how many times a respondent can participate in a specific group.
  - For example, if a respondent is assigned to a group with a participation limit of 1 in an earlier stage, they will not be assigned to that group in later stages.
- Participation limits are set per group in the column **“Participation count\*”**.

<img src="images/participation_limit.png" alt="Participation limit" class="md-image" />

- Group names must be identical across all stages for participation limits to work correctly.

### 2.3 Stage Management

#### 2.3.1 Adding a Stage

- Add a stage by clicking **“Add stage”**. A new table appears for defining the options.

<img src="images/stage.png" alt="Stage" class="md-image" />

#### 2.3.2 Stage Identifier

- Each stage must have a unique identifier (e.g. date or week number).
- Respondents navigate stages using these identifiers, so they should clearly describe the stage.

#### 2.3.3 Adding Options to a Stage

- Options can be added manually or imported from a CSV file, just like in a regular survey.

#### 2.3.4 Copying a Stage

- Click **“Copy stage”** to duplicate a stage and all its data.

#### 2.3.5 Deleting a Stage

- Click **“Delete stage”** to remove a stage.

---

## 3. Managing a Survey

All surveys are listed on the **“View previous surveys”** page.

<img src="images/survey_management.png" alt="Survey management" class="md-image" />

### 3.1 Sending the Survey to Respondents

- Click **“Copy survey link to clipboard”** or copy the URL from the browser address bar.

### 3.2 Closing the Survey

- Open **“View results”** and click **“Close survey”**.

### 3.3 Reopening a Closed Survey

- Click **“Reopen survey”** and confirm.

### 3.4 Granting Administrative Rights

- On the edit page, enter another teacher’s email address and click **“Add teacher”**.

<img src="images/admin.png" alt="Admin rights" class="md-image" />

### 3.5 Editing a Survey

- You can edit the name, description, and response period.
- Group sizes can only be edited if there are more respondents than available places.

### 3.6 Deleting a Survey

- Deleted surveys are moved to the trash and permanently removed after one week.

### 3.7 Restoring a Survey

- Deleted surveys can be restored from the trash.

### 3.8 Copying a Survey

- Click **“Copy survey”** to create a new survey based on an existing one.

---

## 4. Processing Responses

### 4.1 Viewing Responses

- Click **“View results”** on the survey.

### 4.2 Group Allocation

- Close the survey, then click **“Allocate groups”**.

### 4.3 More Responses Than Places

- Edit group sizes if prompted.
- If necessary, an **“Empty”** group is created for unassigned respondents.

### 4.4 Processing Results

- Click **“Save results”** to store the allocation.
- Saved surveys cannot be reopened.
- Results can be exported to Excel.

---

## 5. Answering a Survey

<img src="images/answer.png" alt="Answer survey" class="md-image" />

### 5.1 Ranking Options

- Drag options into the green box and arrange them by preference.

### 5.2 Denying Options

- If allowed, drag options into the red box and provide a justification of at least 10 characters.

---

## 6. Answering a Multi-Stage Survey

<img src="images/multistage_answer.png" alt="Multi-stage answer" class="md-image" />

### 6.1 Stages

- Navigate between stages using the stage identifiers.
- Answer each stage like a regular survey.

### 6.2 Absences

- If allowed, click **“I am absent”** to mark yourself absent.

<img src="images/absence.png" alt="Absence" class="md-image" />
