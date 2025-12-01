const ParseDeleteDate = ({ deletedAt }) => {
  const timestamp = Date.parse(deletedAt);
  const deleteDate = new Date(timestamp);
  deleteDate.setDate(deleteDate.getDate() + 7);

  const day = deleteDate.getDate();
  const month = deleteDate.getMonth() + 1;
  const year = deleteDate.getFullYear();

  return `${day}.${month}.${year} 00:00`;
};

export default ParseDeleteDate;
