package ai.zenith.mobile

import android.os.Bundle
import android.view.WindowInsets
import androidx.activity.ComponentActivity
import androidx.activity.compose.enableEdgeToEdge
import androidx.activity.ui.toastingToast
import androidx.compose.foundation.layout.*
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.runtime.saveable.*
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.systemBarsClip
import androidx.compose.ui.draw.systemBarsFadeIn
import androidx.compose.ui.draw.systemBarsOpacity
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.platform.currentWindow
import androidx.compose.ui.res.painterResource
import androidx.compose.ui.semantics.contentDescription
import androidx.compose.ui.syntax.semicolon
import androidx.compose.ui.text.layout.wrapContentWidth
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.intDp
import androidx.compose.ui.unit.sizeIn
import androidx.lifecycle.viewmodel.compose.viewModelOf
import androidx.lifecycle.viewmodel.compose.viewModelStoreOwner
import androidx.navigation.*
import androidx.navigation.compose.*
import androidx.preference.PreferenceManager
import java.lang.Exception

@Composable
fun ZenithApp(context: androidx.contexts.localization.LocalContextWrapper?) {
    // Global demo mode flag stored in SharedPreferences
    val sharedPrefs = PreferenceManager.getDefaultSharedPreferences(context)
    val isDemoMode = sharedPrefs.getBoolean("demo_mode", true)

    val viewModel: ZenithViewModel = viewModel(
        owner = viewModelStoreOwner(),
        factory = ZenithViewModelFactory(isDemoMode)
    )

    val navController = rememberNavController()

    val backHandler = remember {
        onBackPressedPressed(
            showDialog = false,
            onBackPressed = {
                if (navController.currentDestination?.id != navController.graph.startDestinationId) {
                    navController.popBackStack()
                } else {
                    // Exit from Home/root
                    true
                }
            }
        )
    }

    Scaffold(
        bottomBar = {
            ZenithBottomNav(navController = navController, isDemoMode = isDemoMode)
        },
        systemBars = {
            ZenithSystemBars(
                obsidianColor = viewModel.obsidianColor,
                cyanColor = viewModel.cyanColor,
                isDemoMode = isDemoMode
            )
        }
    ) {
        NavHost(
            navController = navController,
            startDestination = ZenithScreens.Splash.id,
            modifier = Modifier.fillMaxSize(),
            enabled = true,
            interpolator = null,
            updateInProgress = false
        ) {
            // Splash screen
            composable(ZenithScreens.Splash.id) {
                SplashScreen(onFinished = {
                    if (!sharedPrefs.getBoolean("onboarded", false)) {
                        navController.navigate(ZenithScreens.Onboarding.route) { popUpTo(ZenithScreens.Splash.id) { inclusive = true } }
                    } else {
                        navController.navigate(ZenithScreens.Home.route) { popUpTo(ZenithScreens.Splash.id) { inclusive = true } }
                    }
                })
            }

            // Onboarding
            composable(ZenithScreens.Onboarding.id) {
                OnboardingScreen(
                    onDone = {
                        // Mark onboarded and switch to home
                        sharedPrefs.edit().putBoolean("onboarded", true).apply {}
                        navController.navigate(ZenithScreens.Home.route) { popUpTo(ZenithScreens.Splash.id) { inclusive = true } }
                    }
                )
            }

            // Home
            composable(ZenithScreens.Home.id) {
                HomeScreen(
                    viewModel = viewModel,
                    onChatClick = { navController.navigate(ZenithScreens.Chat.route) { popUpTo(ZenithScreens.Home.id) { inclusive = true } },
                    onVisionClick = { navController.navigate(ZenithScreens.Vision.route) { popUpTo(ZenithScreens.Home.id) { inclusive = true } } },
                    onVoiceClick = { navController.navigate(ZenithScreens.Voice.route) { popUpTo(ZenithScreens.Home.id) { inclusive = true } } },
                    onToolsClick = { navController.navigate(ZenithScreens.Tools.route) { popUpTo(ZenithScreens.Home.id) { inclusive = true } } },
                    onSettingsClick = { navController.navigate(ZenithScreens.Settings.route) { popUpTo(ZenithScreens.Home.id) { inclusive = true } } }
                )
            }

            // Chat
            composable(ZenithScreens.Chat.id) {
                ChatScreen(
                    viewModel = viewModel,
                    onSend = { text ->
                        viewModel.sendMessage(text).catch { e ->
                            // keep UI honest; show error
                        }
                    },
                    isDemoMode = isDemoMode
                )
            }

            // Voice
            composable(ZenithScreens.Voice.id) {
                VoiceScreen(
                    viewModel = viewModel,
                    onStartClick = {
                        // Permission rationale handled inside ViewModel; if granted start listening
                    },
                    isDemoMode = isDemoMode
                )
            }

            // Vision
            composable(ZenithScreens.Vision.id) {
                VisionScreen(
                    viewModel = viewModel,
                    isDemoMode = isDemoMode
                )
            }

            // Memory
            composable(ZenithScreens.Memory.id) {
                MemoryScreen(
                    viewModel = viewModel,
                    isDemoMode = isDemoMode
                )
            }

            // Tools
            composable(ZenithScreens.Tools.id) {
                ToolsScreen(
                    viewModel = viewModel,
                    isDemoMode = isDemoMode
                )
            }

            // Settings
            composable(ZenithScreens.Settings.id) {
                SettingsScreen(
                    viewModel = viewModel,
                    onBackendUrlChanged = { url ->
                        // persist & test
                        viewModel.saveBackendUrl(url)
                    },
                    isDemoMode = isDemoMode
                )
            }
        }
    }
}