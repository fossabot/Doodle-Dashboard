Feature: Display output from feeds

  Scenario: One notification writes output to the console
    Given I load test displays
    And I have the configuration called 'config.yml'
      """
      interval: 0
      display: test-display-all-functionality
      data-feeds:
        - source: text
          text:
           - The weather for next week is snow
           - Bob tweeted good morning
        - source: text
          text: World

      notifications:
        - title: Display weather
          type: text
          update-with:
            name: text-from-message
            filter-messages:
              - type: message-contains-text
                text: weather
      """
    When I call 'start --once config.yml'
    Then the status code is 0
    And the output is
      """
      Interval: 0
      Display loaded: test-display-all-functionality
      2 data sources loaded
       - Text
       - Text
      1 notifications loaded
       - Text notification (title=Display weather, text=)
      Dashboard running...
      Displaying Text notification (title=Display weather, text=The weather for next week is snow)

      """

    Scenario: Two notifications writes output to the console
    Given I load test displays
    And I have the configuration called 'config.yml'
      """
      interval: 0
      display: test-display-all-functionality
      data-feeds:
        - source: text
          text:
           - Jenkins build failing
           - Bank balance is £1

      notifications:
        - title: Bank balance
          type: text
          update-with:
            name: text-from-message
            filter-messages:
              - type: message-matches-regex
                pattern: Bank balance is £[0-9]+

        - title: Jenkins build status
          type: text
          update-with:
            name: text-from-message
            filter-messages:
              - type: message-contains-text
                text: Jenkins
      """
    When I call 'start --once config.yml'
    Then the status code is 0
    And the output is
      """
      Interval: 0
      Display loaded: test-display-all-functionality
      1 data sources loaded
       - Text
      2 notifications loaded
       - Text notification (title=Bank balance, text=)
       - Text notification (title=Jenkins build status, text=)
      Dashboard running...
      Displaying Text notification (title=Bank balance, text=Bank balance is £1)
      Displaying Text notification (title=Jenkins build status, text=Jenkins build failing)

      """