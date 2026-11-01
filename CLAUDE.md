# ScreenGuide: instructions for the AI fixer

ScreenGuide is an Android app (Kotlin) that points at the next thing to tap, for first-time smartphone users in Zambia.
The owner is a solo developer who works only on his phone. He reads your issue comments in the GitHub app, so write
them in plain English for a non-specialist.

## How this repository is laid out

- The app's source is **not** in folders. Each version is a zip at the top level: `screenguide-src-v0.55.zip`,
  `screenguide-src-v0.56.zip`, and so on. The highest `vX.YY` number is the current source. Ignore the older,
  unnumbered zips (`screenguide-src-14.zip` etc.) and never change any existing zip.
- The APK build (`.github/workflows/build.yml`) unzips the newest zip into `src/` and runs
  `gradle testDebugUnitTest lintDebug assembleDebug`.
- Unit tests: `app/src/test/java/zm/screenguide/` (JUnit 4, plain JVM, no Android framework).
- Crash reports from phones come from `Guides.kt` (the crash catcher) and `Server.kt` (`/crash`). They hold only code
  places, the app version and the phone kind.

## How to fix a crash

1. Unzip the newest source: `unzip -q screenguide-src-vX.YY.zip -d src`
2. Find the cause from the stack trace in the issue. Our code is under `zm.screenguide`.
3. **Prove it first.** Write a unit test that fails because of the bug, and run it to see it fail:
   `cd src && gradle testDebugUnitTest --no-daemon`. If the crash is in code that only runs on a phone
   (an Activity or the accessibility service), move the faulty logic into a plain function you can test, or explain
   in the issue why a JVM test is not possible.
4. **If you cannot reproduce it, stop.** Say so on the issue, say what extra information would help, and do not guess.
5. Make the smallest change that fixes the cause, not the symptom. Do not rewrite working code or change features.
6. Run everything: `cd src && gradle testDebugUnitTest lintDebug assembleDebug --no-daemon`. All of it must pass.
7. Bump the version in `src/app/build.gradle.kts`: `versionCode` + 1, `versionName` to the next `0.YY`.
8. Save the new source as the next zip, without build output:
   `cd src && zip -qr ../screenguide-src-v0.YY.zip . -x 'app/build/*' 'build/*' '.gradle/*' '*/.gradle/*'`
9. Commit **only** the new zip, with a message like `App v0.56: fix crash when a guide has no next step`.
   Never commit `src/`.

## Rules

- Never delete, skip or weaken a test to make it pass.
- Never change `.github/workflows/` or any older zip.
- One crash per run. If you notice other problems, list them in your comment instead of fixing them.
- The app must keep working on Android 7 (minSdk 24) and on low-end phones (Tecno, Infinix, itel) with weak networks.
- Privacy: never log or send screen words, passwords or personal details. Never weaken the rule that ScreenGuide does not
  guide inside banking or mobile money apps.
- If the fix needs a decision from the owner (it changes what the app does), ask one clear question on the issue and stop.

## What to write on the issue when you finish

1. **What was wrong**, in one or two sentences, and who it affected (which phones, which screen).
2. **Which kind of bug it was**: in our code; caused by Android or a phone maker (then say what the workaround does);
   or needing the owner's decision.
3. **How serious**: High (app closes for many people), Medium, or Low.
4. **What you changed** and **the test that now guards it**.
5. **How sure you are**, and anything you could not check (for example, it only happens on a real phone).
