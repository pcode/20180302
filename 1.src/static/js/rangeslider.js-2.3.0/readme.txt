Usage
Using rangeslider.js is simple. Configuration over attributes.

<input
    type="range"
    min="10"                    // default 0
    max="1000"                  // default 100
    step="10"                   // default 1
    value="300"                 // default min + (max-min)/2
    data-orientation="vertical" // default horizontal
>
<script src="jquery.min.js"></script>
<script src="rangeslider.min.js"></script>
<script>
    // Initialize a new plugin instance for all
    // e.g. $('input[type="range"]') elements.
    $('input[type="range"]').rangeslider();

    // Destroy all plugin instances created from the
    // e.g. $('input[type="range"]') elements.
    $('input[type="range"]').rangeslider('destroy');

    // Update all rangeslider instances for all
    // e.g. $('input[type="range"]') elements.
    // Usefull if you changed some attributes e.g. `min` or `max` etc.
    $('input[type="range"]').rangeslider('update', true);
</script>
Options
$('input[type="range"]').rangeslider({

    // Feature detection the default is `true`.
    // Set this to `false` if you want to use
    // the polyfill also in Browsers which support
    // the native <input type="range"> element.
    polyfill: true,

    // Default CSS classes
    rangeClass: 'rangeslider',
    disabledClass: 'rangeslider--disabled',
    horizontalClass: 'rangeslider--horizontal',
    verticalClass: 'rangeslider--vertical',
    fillClass: 'rangeslider__fill',
    handleClass: 'rangeslider__handle',

    // Callback function
    onInit: function() {},

    // Callback function
    onSlide: function(position, value) {},

    // Callback function
    onSlideEnd: function(position, value) {}
});