package ai.zenith.mobile

import android.app.Application

class ZenithApplication : Application() {
    override fun onCreate() {
        super.onCreate()
        // Application‑level initialization (e.g., localization, logging) goes here.
        // Provider credentials are never embedded in the app; they live on the server.
    }
}