# Below are normally provided by Chromium's base.gyp and required for
# libjingle.gyp.
{
  'targets': [
    {
      'target_name': 'base',
      'type': 'none',
      'direct_dependent_settings': {
        'include_dirs': [
          '..',
        ],
      },
      'conditions': [
        ['OS == "linux"', {
          'link_settings': {
            'libraries': [
              # We need rt for clock_gettime() used in libjingle.
              '-lrt',
            ],
          },
        }],
        ['OS == "mac"', {
          'link_settings': {
            'libraries': [
              '$(SDKROOT)/System/Library/Frameworks/CoreFoundation.framework',
              '$(SDKROOT)/System/Library/Frameworks/CoreServices.framework',
              '$(SDKROOT)/System/Library/Frameworks/Foundation.framework',
            ],
          },
        }],
      ],
    },
  ],
}
