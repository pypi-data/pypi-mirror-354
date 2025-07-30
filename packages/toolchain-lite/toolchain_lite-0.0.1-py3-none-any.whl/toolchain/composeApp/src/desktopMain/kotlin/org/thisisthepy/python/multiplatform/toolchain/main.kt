package org.thisisthepy.python.multiplatform.toolchain

import androidx.compose.ui.window.Window
import androidx.compose.ui.window.application

fun main() = application {
    Window(
        onCloseRequest = ::exitApplication,
        title = "toolchain",
    ) {
        App()
    }
}