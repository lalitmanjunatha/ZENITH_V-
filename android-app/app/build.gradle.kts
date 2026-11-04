plugins {
    id("com.android.application")
    id("org.jetbrains.kotlin.android")
    id("org.jetbrains.kotlin.plugin.compose")
}

android {
    namespace = "ai.zenith.mobile"
    compileOptions {
        sourceCompatibility JavaVersion.VERSION_17
        targetCompatibility JavaVersion.VERSION_17
    }
    kotlinOptions {
        jvmTarget = "17"
    }

    defaultConfig {
        applicationId = "ai.zenith.mobile"
        minSdk = 26
        targetSdk = 35
        versionCode = 1
        versionName = "1.0.0"
    }
}

plugins {
    id("com.google.protobuf") version "0.8.19" apply false
    id("jacoco") version "0.8.9" apply false
}

dependencies {
    // Compose BOM
    platform("androidx.compose:compose-bom:2024.09.00")
    implementation("androidx.compose.ui:ui")
    implementation("androidx.compose.foundation:foundation")
    implementation("androidx.compose.material3:material3")
    implementation("androidx.compose.runtime:runtime")
    implementation("androidx.compose.animation:animation")
    implementation("androidx.activity:activity-compose")
    implementation("androidx.navigation:navigation-compose")
    implementation("androidx.lifecycle:lifecycle-runtime-ktx")
    implementation("androidx.lifecycle:lifecycle-viewmodel-compose")
    implementation("androidx.core:core-ktx")
    implementation("org.jetbrains.kotlinx:kotlinx-coroutines-android")
    debugImplementation("androidx.compose.ui:ui-tooling-preview")
}