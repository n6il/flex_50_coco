ZIPS=( 'Color FLEX 5.0:4 (Frank Hogg Laboratory)' \
	'Color Utilities (FLEX)(Frank Hogg Laboratory)'
	'ED Editor (FLEX)(Frank Hogg Laboratory)'
	'Extended 6809 BASIC (FLEX)(Technical Systems Consultants)'
	)

for n in "${ZIPS[@]}"; do
	echo "=== $n ==="
	rm "${n}.zip"
	zip -r "${n}.zip" "${n}"
done
