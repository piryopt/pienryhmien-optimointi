const Table = ({
  columns,
  data,
  renderRow,
  className = "table table-striped",
  cellSpacing = 10
}) => {
  return (
    <table cellSpacing={cellSpacing} className={className}>
      <thead className="table-dark">
        <tr>
          {columns.map((col, i) => (
            <th key={i} style={col.style || null}>
              <p>
                <img
                  src={col.logo}
                  width={24}
                  height={24}
                  className="d-inline-block align-text-top"
                />
                &nbsp;{col.title}
              </p>
            </th>
          ))}
        </tr>
      </thead>
      <tbody>{data.map((item, i) => renderRow(item, i))}</tbody>
    </table>
  );
};

export default Table;
