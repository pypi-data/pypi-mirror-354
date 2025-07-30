package org.thisisthepy.python.multiplatform.toolchain

interface Platform {
    val name: String
}

expect fun getPlatform(): Platform