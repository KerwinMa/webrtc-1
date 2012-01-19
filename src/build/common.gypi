# Copyright (c) 2011 The WebRTC project authors. All Rights Reserved.
#
# Use of this source code is governed by a BSD-style license
# that can be found in the LICENSE file in the root of the source
# tree. An additional intellectual property rights grant can be found
# in the file PATENTS.  All contributing project authors may
# be found in the AUTHORS file in the root of the source tree.

# This file contains common settings for building WebRTC components.

{
  'variables': {
    # These variables need to be nested in order to use them in a conditions
    # block to set other variables.
    'variables': {
      # This will be set to zero in the supplement.gypi triggered by a gclient
      # hook in the standalone build.
      'build_with_chromium%': 1,
    },

    'build_with_chromium%': '<(build_with_chromium)',

    # The Chromium common.gypi we use treats all gyp files without
    # chromium_code==1 as third party code. This disables many of the
    # preferred warning settings.
    #
    # We can set this here to have WebRTC code treated as Chromium code. Our
    # third party code will still have the reduced warning settings.
    'chromium_code': 1,

    # Adds video support to dependencies shared by voice and video engine.
    # This should normally be enabled; the intended use is to disable only
    # when building voice engine exclusively.
    'enable_video%': 1,

    # Selects fixed-point code where possible.
    # TODO(andrew): we'd like to set this based on the target OS/architecture.
    'prefer_fixed_point%': 0,

    # Enable data logging. Produces text files with data logged within engines
    # which can be easily parsed for offline processing.
    'enable_data_logging%': 0,

    # Disable these to not build components which can be externally provided.
    'build_libjpeg%': 1,
    'build_libyuv%': 1,

    'conditions': [
      ['OS=="win"', {
        # TODO(andrew, perkj): does this need to be here?
        # Path needed to build Direct Show base classes on Windows.
        # The code is included in the Windows SDK.
        'direct_show_base_classes':
          'C:/Program Files/Microsoft SDKs/Windows/v7.1/Samples/multimedia/directshow/baseclasses/',
      }],
      ['build_with_chromium==1', {
        # Exclude pulse audio on Chromium since its prerequisites don't require
        # pulse audio.
        'include_pulse_audio%': 0,

        # Exclude internal ADM since Chromium uses its own IO handling.
        'include_internal_audio_device%': 0,

        # Exclude internal VCM in Chromium build.
        'include_internal_video_capture%': 0,

        # Exclude internal video render module in Chromium build.
        'include_internal_video_render%': 0,

        # Disable the use of protocol buffers in production code.
        'enable_protobuf%': 0,

        'webrtc_root%': '<(DEPTH)/third_party/webrtc',
      }, {
        # Settings for the standalone (not-in-Chromium) build.

        'include_pulse_audio%': 1,

        'include_internal_audio_device%': 1,

        'include_internal_video_capture%': 1,

        'include_internal_video_render%': 1,

        'enable_protobuf%': 1,

        'webrtc_root%': '<(DEPTH)/src',

        'conditions': [
          ['OS=="mac"', {
            # TODO(andrew): clang is the default on Mac. For now, disable the
            # Chrome plugins, which causes a flood of chromium-style warnings.
            # Investigate enabling the plugins:
            # http://code.google.com/p/webrtc/issues/detail?id=163
            'clang_use_chrome_plugins%': 0,
          }],
        ],
      }],
    ], # conditions
  },
  'target_defaults': {
    'include_dirs': [
      '..','../..', # common_types.h, typedefs.h
    ],
    'conditions': [
      ['build_with_chromium==1', {
        'defines': [
          # Changes settings for Chromium build.
          'WEBRTC_CHROMIUM_BUILD',
        ],
      }, {
        'conditions': [
          ['os_posix==1', {
            'cflags': [
              '-Wextra',
              # We need to repeat some flags from Chromium's common.gypi here
              # that get overridden by -Wextra.
              '-Wno-unused-parameter',
              '-Wno-missing-field-initializers',
            ],
          }],
        ],
      }],
      ['OS=="linux"', {
        'defines': [
          'WEBRTC_TARGET_PC',
          'WEBRTC_LINUX',
          'WEBRTC_THREAD_RR',
          # TODO(andrew): can we select this automatically?
          # Define this if the Linux system does not support CLOCK_MONOTONIC.
          #'WEBRTC_CLOCK_TYPE_REALTIME',
        ],
      }],
      ['OS=="mac"', {
        # TODO(andrew): what about PowerPC?
        # Setup for Intel
        'defines': [
          'WEBRTC_TARGET_MAC_INTEL',
          'WEBRTC_MAC_INTEL',
          'WEBRTC_MAC',
          'WEBRTC_THREAD_RR',
          'WEBRTC_CLOCK_TYPE_REALTIME',
        ],
      }],
      ['OS=="win"', {
        'defines': [
          'WEBRTC_TARGET_PC',
        ],
        # TODO(andrew): remove this block when possible.
        'msvs_disabled_warnings': [4389], # Signed/unsigned mismatch.
        'msvs_settings': {
          'VCCLCompilerTool': {
            'WarnAsError': 'false',
          },
        },
      }],
    ], # conditions
  }, # target_defaults
}

