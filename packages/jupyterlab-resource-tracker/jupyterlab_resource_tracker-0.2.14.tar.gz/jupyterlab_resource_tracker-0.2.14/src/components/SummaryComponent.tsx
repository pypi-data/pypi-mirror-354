import React from 'react';
import { Paper, Typography } from '@mui/material';
import {
  DataGrid,
  GridColDef,
  GridFooterContainer,
  useGridApiContext,
  useGridSelector,
  gridFilteredSortedRowEntriesSelector
} from '@mui/x-data-grid';
import { Summary } from '../common/types';

interface SummaryComponentProps {
  summary: Summary[];
  loading: boolean;
}

const SummaryComponent: React.FC<SummaryComponentProps> = (
  props
): JSX.Element => {
  const columns: GridColDef[] = [
    { field: 'id', headerName: 'ID', width: 70 },
    { field: 'project', headerName: 'Project', width: 130 },
    { field: 'podName', headerName: 'Username', width: 150 },
    { field: 'usage', headerName: 'Usage (Hours)', type: 'number', width: 130 },
    {
      field: 'cost',
      headerName: 'Cost',
      type: 'number',
      width: 130
    },
    { field: 'month', headerName: 'Month', width: 60, align: 'center' },
    { field: 'year', headerName: 'Year', width: 60, align: 'center' },
    { field: 'lastUpdate', headerName: 'Updated', width: 270 }
  ];

  const paginationModel = { page: 0, pageSize: 10 };

  function CustomFooter() {
    const apiRef = useGridApiContext();
    const rows = useGridSelector(apiRef, gridFilteredSortedRowEntriesSelector);
    const totalUsage = rows.reduce(
      (sum, rowEntry) => sum + (rowEntry.model.usage ?? 0),
      0
    );
    const totalCost = rows.reduce(
      (sum, rowEntry) => sum + (rowEntry.model.cost ?? 0),
      0
    );

    return (
      <GridFooterContainer>
        <div
          style={{
            width: '100%',
            display: 'flex',
            justifyContent: 'flex-start',
            gap: '1rem',
            paddingLeft: '1rem'
          }}
        >
          <Typography variant="subtitle1">
            <strong>Total Usage (Hours):</strong> {totalUsage.toFixed(2)}
          </Typography>
          <Typography variant="subtitle1">
            <strong>Total Cost:</strong> {totalCost.toFixed(2)}
          </Typography>
        </div>
      </GridFooterContainer>
    );
  }

  return (
    <React.Fragment>
      <Typography variant="h6" gutterBottom>
        Monthly costs and usages to date
      </Typography>
      <Paper sx={{ p: 2, boxShadow: 3, borderRadius: 2, mb: 2 }}>
        <DataGrid
          slots={{ footer: CustomFooter }}
          autoHeight
          rows={props.summary}
          columns={columns}
          loading={props.loading}
          initialState={{
            pagination: { paginationModel },
            columns: {
              columnVisibilityModel: {
                id: false
              }
            }
          }}
          pageSizeOptions={[10, 20, 30]}
          disableRowSelectionOnClick
          sx={{ border: 0 }}
        />
      </Paper>
    </React.Fragment>
  );
};

export default SummaryComponent;
