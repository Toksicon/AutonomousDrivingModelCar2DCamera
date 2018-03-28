# NXP Cup Alamak Project

## Setup

### Import Project into CodeWarrior Workspace

Select a workspace location.

In the menubar: ``File`` > ``Import``

In the Import window: ``General`` > ``Existing Projects into Workspace``

Select the ``$$YOUR_REPOSITORY_PATH$$/src/NXP_Cup_Alamak_Minimal`` directory as root directory.

Check that the project is selected in the list of projects.

Check that ``Copy projects into workspace`` is disabled. We want to edit sources in the repository.

Press ``Finish``.


### Flash File To Target

* Select the File to Flash:
``${workspace_loc:/NXP_Cup_Alamak_Minimal/FLASH/NXP_Cup_Alamak_Minimal.elf}``

* Enter a Task Name

* Press ``Erase and Program``

* Select save resource to framework only and press ``OK``.


### Debug

If debug fails on pressing the debug button. Open the ``Debug Configurations``.

You have to select an application for the task, created in the ``Flash File To Target`` step.

Do this by pressing the ``Search Project...`` button and select the ``NXP_Cup_Alamak_Minimal.elf`` binary.

Apply the changes and press ``Debug``.
