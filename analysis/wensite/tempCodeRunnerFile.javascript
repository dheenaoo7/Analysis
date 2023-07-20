var sortedKeys = Object.entries(keyValueObject).sort(function(a, b) {
        return b[1] - a[1];
      });
      var sortedKeyValueObject = {};
      var a = 0;

for (var i = 0; i < sortedKeys.length; i++) {
  if (a === 9) {
    break;
  }

  var key = sortedKeys[i][0];
  var value = sortedKeys[i][1];
  a++;
  sortedKeyValueObject[key] = value;
}

      console.log(sortedKeyValueObject);