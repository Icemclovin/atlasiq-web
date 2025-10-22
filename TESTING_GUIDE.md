# 🧪 Testing the Macro Economic Indicators Feature

Quick guide to test the new macro indicators frontend.

---

## ✅ Pre-Testing Checklist

### Servers Running?
- [ ] **Backend**: http://localhost:8000 ✓
- [ ] **Frontend**: http://localhost:3000 ✓

**Check terminals**:
- Backend should show: `✅ Database connection healthy`
- Frontend should show: `ready in XXX ms`

---

## 🎯 Test Scenarios

### 1. Login & Access Dashboard
1. Navigate to http://localhost:3000
2. Login with test credentials
3. Verify dashboard loads successfully
4. Scroll down to see **"Economic Indicators"** section

**Expected**: Full dashboard with macro indicators widget at bottom

---

### 2. GDP Growth Tab (Default)
1. Widget should load with **GDP Growth** tab active
2. Chart displays data for all 4 countries by default
3. Look for these data points:
   - **Netherlands (Orange line)**: ~-4% in 2020 (COVID dip)
   - **Netherlands**: ~+5% in 2021 (recovery)

**Expected**: Line chart with 4 colored lines (NLD, BEL, LUX, DEU)

---

### 3. Inflation Tab
1. Click **"Inflation"** tab
2. Chart should update to show inflation rates
3. Look for spike in 2022:
   - **Netherlands**: ~10% (inflation crisis)
   - **Belgium**: ~9-10%

**Expected**: Chart shows dramatic increase in 2022

---

### 4. Unemployment Tab
1. Click **"Unemployment"** tab
2. Chart shows unemployment rates
3. Verify low rates in 2023:
   - **Netherlands**: ~3.5%
   - **Germany**: ~3.0%

**Expected**: Relatively flat lines with low values

---

### 5. Interest Rates Tab
1. Click **"Interest Rates"** tab
2. Should show ECB rates (no country filter needed)
3. Look for rate hikes in 2022-2023:
   - **Deposit Facility**: 0% → 4%
   - **Main Refinancing**: 0% → 4.5%

**Expected**: Three lines showing dramatic increase from ~0% to ~4%

---

## 🎨 UI Control Testing

### Country Filters (GDP/Inflation/Unemployment tabs)
1. **Uncheck "Netherlands"** - orange line disappears
2. **Uncheck "Belgium"** - blue line disappears
3. **Try to uncheck last country** - should stay checked (minimum 1 required)
4. **Re-check countries** - lines reappear

**Expected**: Chart dynamically updates based on selection

---

### Date Range Selectors
1. **Change Start Year to 2020**
2. **Change End Year to 2022**
3. Chart should only show 2020-2022 data

**Expected**: X-axis shows only selected years

---

### Chart Type Toggle
1. Click **"Bar"** button
2. Chart changes to bar chart
3. Click **"Area"** button
4. Chart changes to area chart with gradient fill
5. Click **"Line"** button
6. Returns to line chart

**Expected**: Smooth transitions between chart types

---

### CSV Export
1. Click **"Export CSV"** button
2. File downloads to your Downloads folder
3. Open CSV file
4. Verify data structure:
   ```csv
   year,NLD,BEL,LUX,DEU
   2015,2.3,2.0,4.3,1.5
   ```

**Expected**: CSV file with correct data

---

## 🔍 Visual Inspection

### Check These Elements
- [ ] **Historical Data Badge** - Blue badge showing "Historical Data"
- [ ] **Tab Highlighting** - Active tab has blue underline
- [ ] **Chart Grid Lines** - Visible and readable
- [ ] **Legend** - Shows country codes with correct colors
- [ ] **Tooltips** - Hover over chart points to see values
- [ ] **Y-axis Labels** - Shows correct units (%, Growth Rate, etc.)
- [ ] **Loading Spinner** - Visible when switching tabs (if network is slow)

---

## 🐛 Error Testing

### Test Error Handling
1. **Stop the backend server** (Ctrl+C in backend terminal)
2. **Switch tabs** in frontend
3. Should show error message: "Failed to load data. Please try again."
4. **Click "Try again"** button (will still fail)
5. **Restart backend server**
6. **Click "Try again"** - data should load

**Expected**: Graceful error messages, no crashes

---

## 📱 Responsive Design Testing

### Desktop (Current)
- [ ] Chart fills container width
- [ ] All controls visible
- [ ] No horizontal scrolling

### Tablet (Resize browser to ~768px)
- [ ] Layout adjusts
- [ ] Chart remains readable
- [ ] Filters stack vertically

### Mobile (Resize browser to ~375px)
- [ ] Widget is scrollable
- [ ] Tabs are tappable
- [ ] Chart is zoomable/scrollable

---

## ✨ Advanced Testing

### Performance
1. **Switch between tabs rapidly** - should be smooth
2. **Toggle all country filters** - updates quickly
3. **Change date ranges multiple times** - no lag

### Data Accuracy
Compare displayed values with backend API:

**Test GDP 2020 for Netherlands**:
1. Backend: `curl http://localhost:8000/api/v1/macro/gdp?countries=NLD&start_year=2020&end_year=2020`
2. Frontend: Check chart tooltip for NLD 2020
3. **Values should match**: -3.9%

---

## 🎯 Expected Results Summary

| Test | Expected Result | Pass/Fail |
|------|-----------------|-----------|
| Dashboard loads | Macro widget visible | |
| GDP chart displays | 4 countries, COVID dip visible | |
| Inflation chart | 2022 spike visible | |
| Unemployment chart | Low rates ~3-4% | |
| Interest rates chart | 2022-23 rate hikes visible | |
| Country filters work | Lines add/remove dynamically | |
| Date range works | Chart updates to selected years | |
| Chart types toggle | Smooth transitions | |
| CSV export | File downloads with data | |
| Error handling | Error message + retry button | |
| Loading states | Spinner visible during fetch | |
| Responsive design | Works on different screen sizes | |

---

## 🚨 Common Issues & Solutions

### Issue: "Cannot find module 'recharts'"
**Solution**: Run `npm install` in frontend directory

### Issue: "CORS error" in browser console
**Solution**: Check backend CORS settings include `http://localhost:3000`

### Issue: Chart shows "No data available"
**Solution**: 
1. Check backend is running
2. Verify API endpoints work: http://localhost:8000/docs
3. Check browser console for errors

### Issue: CSV export doesn't work
**Solution**: 
1. Check browser's download settings
2. Ensure pop-ups aren't blocked
3. Verify data is loaded before exporting

---

## 📊 Data Validation Reference

### Correct Values to Look For

**GDP 2020 (COVID Impact)**:
- NLD: -3.9%
- BEL: -5.4%
- LUX: -1.8%
- DEU: -3.7%

**Inflation 2022 (Spike)**:
- NLD: ~10.0%
- BEL: ~9.6%
- LUX: ~6.3%
- DEU: ~8.7%

**ECB Interest Rates 2023**:
- Deposit Facility: ~4.0%
- Main Refinancing: ~4.5%
- Marginal Lending: ~4.75%

---

## ✅ Testing Complete Checklist

After testing, you should have verified:
- [ ] All 4 indicator tabs work
- [ ] Country filtering functions correctly
- [ ] Date range selection works
- [ ] All 3 chart types display properly
- [ ] CSV export downloads data
- [ ] Error handling shows appropriate messages
- [ ] Loading states appear during data fetching
- [ ] Tooltips show correct values
- [ ] Historical data badge is visible
- [ ] Design is responsive

---

## 🎉 Next Steps After Testing

If all tests pass:
1. **Document any issues** found
2. **Take screenshots** of the working feature
3. **Test with real users** for UX feedback
4. **Proceed to Phase 6** (Testing & Polish)

If tests fail:
1. **Note which tests failed**
2. **Check browser console** for errors
3. **Verify server logs** for API errors
4. **Report issues** for debugging

---

**Happy Testing!** 🚀

For issues or questions, check:
- `PHASE5_FRONTEND_COMPLETE.md` - Full feature documentation
- `DATA_SOURCES.md` - Data source information
- Backend API docs: http://localhost:8000/docs
